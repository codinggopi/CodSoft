const API_URL = "http://127.0.0.1:8000";

window.demoJobs = [
    { id: 'demo-1', title: 'Frontend Developer', company: 'TechNova', location: 'San Francisco, CA', salary: '$120k - $140k', job_type: 'Full Time', skills: 'React, HTML, CSS', description: 'Build beautiful UIs.', requirements: '3+ years React' },
    { id: 'demo-2', title: 'Backend Developer', company: 'CloudSync', location: 'Remote', salary: '$130k - $160k', job_type: 'Full Time', skills: 'Python, Django', description: 'Scale our cloud infrastructure.', requirements: '5+ years Python' },
    { id: 'demo-3', title: 'UI/UX Designer', company: 'ByteWorks', location: 'New York, NY', salary: '$90k - $120k', job_type: 'Full Time', skills: 'Figma, Sketch', description: 'Design engaging user experiences.', requirements: 'Portfolio required' },
    { id: 'demo-4', title: 'Data Analyst', company: 'FutureSoft', location: 'London, UK', salary: '£60k - £80k', job_type: 'Full Time', skills: 'SQL, Python, Tableau', description: 'Analyze product data and create dashboards.', requirements: 'Strong SQL skills' },
    { id: 'demo-5', title: 'Python Developer', company: 'InnoTech', location: 'Austin, TX', salary: '$110k - $130k', job_type: 'Full Time', skills: 'FastAPI, AWS', description: 'Develop backend APIs.', requirements: 'FastAPI experience' },
    { id: 'demo-6', title: 'Full Stack Developer', company: 'DigitalEdge', location: 'Toronto, CA', salary: '$100k - $125k', job_type: 'Remote', skills: 'MERN Stack', description: 'Build end-to-end features.', requirements: 'MongoDB, Express, React, Node' }
];

window.generateJobCard = function(job, isDemo = false) {
    // Generate a placeholder logo character based on company name
    const initial = job.company ? job.company.charAt(0).toUpperCase() : 'C';
    // Simple hash for consistent colors
    const colors = [
        { bg: 'rgba(22, 101, 52, 0.1)', text: '#166534' },
        { bg: 'rgba(13, 148, 136, 0.1)', text: '#0D9488' },
        { bg: 'rgba(245, 158, 11, 0.1)', text: '#F59E0B' },
        { bg: 'rgba(59, 130, 246, 0.1)', text: '#3B82F6' },
        { bg: 'rgba(239, 68, 68, 0.1)', text: '#EF4444' },
        { bg: 'rgba(139, 92, 246, 0.1)', text: '#8B5CF6' }
    ];
    const color = colors[job.company.charCodeAt(0) % colors.length];

    const badgesHtml = `
        <span class="badge badge-primary">${job.job_type}</span>
        ${job.skills ? `<span class="badge badge-warning">${job.skills.split(',')[0]}</span>` : ''}
        ${isDemo ? `<span class="badge" style="background: var(--danger); color: white;">Demo Job</span>` : ''}
    `;

    return `
        <div class="card job-card flex flex-col justify-between">
            <div>
                <div class="flex justify-between items-start mb-4">
                    <div class="flex gap-4 items-center">
                        <div class="company-logo-placeholder" style="background: ${color.bg}; color: ${color.text};">${initial}</div>
                        <div>
                            <h3 style="font-size: 1.1rem; color: var(--text-color); margin-bottom: 0.25rem;">${job.title}</h3>
                            <div class="flex items-center gap-2">
                                <p class="text-muted" style="font-size: 0.875rem; margin: 0;">${job.company}</p>
                                ${!isDemo && job.employer_id ? `<a href="public-company-profile.html?employer_id=${job.employer_id}" style="font-size: 0.75rem; color: var(--primary-color); text-decoration: underline;"><i class="fas fa-external-link-alt"></i></a>` : ''}
                            </div>
                        </div>
                    </div>
                    <button class="btn btn-outline" style="padding: 0.25rem 0.5rem; border-color: var(--border-color); color: var(--text-muted);"><i class="far fa-bookmark"></i></button>
                </div>
                <div class="flex gap-4 text-muted mb-4" style="font-size: 0.875rem; flex-wrap: wrap;">
                    <span><i class="fas fa-map-marker-alt mr-2"></i>${job.location}</span>
                    <span><i class="fas fa-money-bill-wave mr-2"></i>${job.salary}</span>
                </div>
                <div class="flex gap-2 mb-4 flex-wrap">
                    ${badgesHtml}
                </div>
            </div>
            <a href="job-details.html?id=${job.id}" class="btn btn-primary w-full text-center">View Details</a>
        </div>
    `;
};

document.addEventListener('DOMContentLoaded', () => {
    const jobsList = document.getElementById('jobsList');
    if (jobsList) {
        fetchJobs();
    }

    const searchForm = document.getElementById('searchForm');
    if (searchForm) {
        searchForm.addEventListener('submit', (e) => {
            e.preventDefault();
            fetchJobs();
        });
    }

    // Update login link if logged in
    const token = localStorage.getItem('token');
    const userStr = localStorage.getItem('user');
    const loginLink = document.getElementById('loginLink');
    if (token && userStr && loginLink) {
        const user = JSON.parse(userStr);
        loginLink.textContent = "Dashboard";
        if (user.role === 'admin') loginLink.href = 'admin-dashboard.html';
        else if (user.role === 'employer') loginLink.href = 'employer-dashboard.html';
        else loginLink.href = 'candidate-dashboard.html';
    }
});

async function fetchJobs() {
    const jobsList = document.getElementById('jobsList');
    if (!jobsList) return;

    // Read filters from DOM if they exist
    const keywordInput = document.getElementById('searchKeyword');
    const locationInput = document.getElementById('searchLocation');
    const typeInput = document.getElementById('searchType');
    const experienceInput = document.getElementById('searchExperience');
    const remoteInput = document.getElementById('searchRemote');
    
    const keyword = keywordInput ? keywordInput.value.toLowerCase() : '';
    const locationStr = locationInput ? locationInput.value.toLowerCase() : '';
    const type = typeInput ? typeInput.value : '';
    const experience = experienceInput ? experienceInput.value : '';
    const isRemote = remoteInput ? remoteInput.checked : false;
    
    // Check if on home page
    const isHomePage = window.location.pathname.endsWith('index.html') || window.location.pathname === '/';

    try {
        const response = await fetch(`${API_URL}/jobs/`);
        let jobs = [];
        if (response.ok) {
            jobs = await response.json();
            
            // Filter real jobs
            if (keyword) jobs = jobs.filter(j => j.title.toLowerCase().includes(keyword) || j.company.toLowerCase().includes(keyword) || j.skills.toLowerCase().includes(keyword));
            if (locationStr) jobs = jobs.filter(j => j.location.toLowerCase().includes(locationStr));
            if (type) jobs = jobs.filter(j => j.job_type === type);
            if (experience) jobs = jobs.filter(j => (j.description || '').includes(experience) || (j.requirements || '').includes(experience));
            if (isRemote) jobs = jobs.filter(j => j.location.toLowerCase().includes('remote') || j.job_type.toLowerCase() === 'remote');
        }
        
        // Apply limit for Home Page
        if (isHomePage && jobs.length > 0) {
            jobs = jobs.slice(0, 3);
        }

        // Update Job Count if it exists
        const countSpan = document.getElementById('jobsCount');

        if (jobs.length > 0) {
            if (countSpan) countSpan.textContent = jobs.length;
            jobsList.innerHTML = jobs.map(job => window.generateJobCard(job, false)).join('');
        } else {
            // Render Demo Jobs if no real jobs exist
            let dJobs = window.demoJobs;
            if (keyword) dJobs = dJobs.filter(j => j.title.toLowerCase().includes(keyword) || j.company.toLowerCase().includes(keyword));
            if (locationStr) dJobs = dJobs.filter(j => j.location.toLowerCase().includes(locationStr));
            if (type) dJobs = dJobs.filter(j => j.job_type === type);
            if (isRemote) dJobs = dJobs.filter(j => j.location.toLowerCase().includes('remote') || j.job_type.toLowerCase() === 'remote');
            
            if (isHomePage) {
                dJobs = dJobs.slice(0, 3);
            }

            if (countSpan) countSpan.textContent = dJobs.length;

            if (dJobs.length === 0) {
                jobsList.innerHTML = `<div style="grid-column: 1 / -1; padding: 4rem 1rem; text-align: center; background: var(--input-bg); border-radius: 0.5rem;">
                    <i class="fas fa-search text-muted mb-4" style="font-size: 2.5rem;"></i>
                    <h3 class="mb-2">No jobs found</h3>
                    <p class="text-muted">Try adjusting your search filters.</p>
                </div>`;
                return;
            }

            // New Empty State Professional Layout
            const emptyStateBanner = !isHomePage ? `
                <div style="grid-column: 1 / -1; width: 100%; background: linear-gradient(to right, rgba(59, 130, 246, 0.1), rgba(37, 99, 235, 0.05)); border-left: 4px solid var(--primary-color); padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex; align-items: center; gap: 1rem;">
                    <div style="font-size: 2rem;">🚀</div>
                    <div>
                        <h4 style="color: var(--primary-color); margin-bottom: 0.25rem;">New opportunities are coming soon.</h4>
                        <p style="color: var(--text-color); font-size: 0.9rem;">Browse featured opportunities while employers post openings.</p>
                    </div>
                </div>
            ` : '';

            jobsList.innerHTML = emptyStateBanner + dJobs.map(job => window.generateJobCard(job, true)).join('');
        }
    } catch (error) {
        console.error("Error fetching jobs:", error);
        jobsList.innerHTML = `<p class="text-danger">Error connecting to server.</p>`;
    }
}
