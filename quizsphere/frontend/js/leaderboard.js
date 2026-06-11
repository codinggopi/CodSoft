// Leaderboard Logic for QuizSphere SaaS
document.addEventListener('DOMContentLoaded', async () => {
    const leaderboardBody = document.getElementById('leaderboard-body');
    const podiumContainer = document.getElementById('podium-container');
    
    if (leaderboardBody && podiumContainer) {
        try {
            const response = await fetch(`${API_URL}/leaderboard/`);
            const entries = await response.json();
            
            // Render Podium (Top 3)
            const top3 = entries.slice(0, 3);
            renderPodium(top3);

            // Render Table (Rank 4+)
            const rest = entries.slice(3);
            leaderboardBody.innerHTML = '';
            
            if (rest.length === 0 && top3.length === 0) {
                leaderboardBody.innerHTML = '<tr><td colspan="5" class="text-center p-5">No leaderboard data yet. Be the first!</td></tr>';
            }

            rest.forEach(entry => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td><span class="rank-badge">${entry.rank}</span></td>
                    <td>
                        <div class="user-cell">
                            <div class="avatar-sm">${entry.user_name.charAt(0)}</div>
                            <span>${entry.user_name}</span>
                        </div>
                    </td>
                    <td>${entry.quiz_name}</td>
                    <td>${entry.score}</td>
                    <td><span class="badge">${entry.percentage.toFixed(1)}%</span></td>
                `;
                leaderboardBody.appendChild(row);
            });
        } catch (err) {
            console.error(err);
        }
    }

    function renderPodium(top3) {
        if (top3.length === 0) {
            podiumContainer.style.display = 'none';
            return;
        }

        // Reorder for display: 2, 1, 3
        const displayOrder = [];
        if (top3[1]) displayOrder.push(top3[1]);
        if (top3[0]) displayOrder.push(top3[0]);
        if (top3[2]) displayOrder.push(top3[2]);

        podiumContainer.innerHTML = '';
        displayOrder.forEach(entry => {
            const isFirst = entry.rank === 1;
            const item = document.createElement('div');
            item.className = `podium-item ${isFirst ? 'podium-first' : ''}`;
            item.innerHTML = `
                <div class="podium-user">
                    <div class="avatar-lg">${entry.user_name.charAt(0)}</div>
                    <div class="font-bold">${entry.user_name}</div>
                </div>
                <div class="podium-rank rank-${entry.rank}">
                    <span class="podium-num">${entry.rank}</span>
                    <span class="podium-score">${entry.percentage.toFixed(1)}%</span>
                </div>
            `;
            podiumContainer.appendChild(item);
        });
    }
});
