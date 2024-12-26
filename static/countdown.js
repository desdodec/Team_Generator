document.getElementById('generateTeams').addEventListener('click', () => {
  const numTeams = document.getElementById('numTeams').value;

  const data = {
    numTeams: numTeams,
    members: [
      'Fergus',
      'Douglas',
      'Elsie',
      'Graham',
      'Sarah',
      'Stanley',
      'Nigel',
      'Helen',
    ],
    excludePair: [], // Add logic to set this dynamically
  };

  fetch('/generate-teams', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((teams) => {
      const teamsDiv = document.getElementById('teams');
      teamsDiv.innerHTML = '';
      teams.forEach((team, index) => {
        const teamDiv = document.createElement('div');
        teamDiv.innerHTML = `<h3>Team ${index + 1}</h3>`;
        team.forEach((member) => {
          const memberDiv = document.createElement('div');
          memberDiv.textContent = member;
          teamDiv.appendChild(memberDiv);
        });
        teamsDiv.appendChild(teamDiv);
      });
    });
});
