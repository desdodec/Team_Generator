const family1Children = ['Fergus', 'Douglas', 'Elise'];
const family1Parents = ['Graham', 'Sarah'];
const family2Children = ['Stanley'];
const family2Parents = ['Nigel', 'Helen'];
let currentTeams = [];

document
  .getElementById('createTeamsButton')
  .addEventListener('click', createTeams);
document
  .getElementById('nextButton')
  .addEventListener('click', displayCountdownWindow);

function createTeams() {
  const children = [...family1Children, ...family2Children];
  const parents = [...family1Parents, ...family2Parents];

  const member1 = document.getElementById('member1').value;
  const member2 = document.getElementById('member2').value;
  const numTeams = parseInt(document.getElementById('numTeams').value);

  children.sort(() => Math.random() - 0.5);
  parents.sort(() => Math.random() - 0.5);

  const teams = Array.from({ length: numTeams }, () => []);
  parents.forEach((parent, index) => {
    teams[index % numTeams].push(parent);
  });

  if (children.includes(member1) && children.includes(member2)) {
    teams[0].push(member1);
    teams[1 % numTeams].push(member2);
    children.splice(children.indexOf(member1), 1);
    children.splice(children.indexOf(member2), 1);
  }

  const distribution = Array(numTeams).fill(0);
  for (let i = 0; i < children.length; i++) {
    const smallestTeam = distribution.indexOf(Math.min(...distribution));
    teams[smallestTeam].push(children[i]);
    distribution[smallestTeam]++;
  }

  currentTeams = teams;
  displayTeams(teams);

  document.getElementById('nextButton').style.display = 'inline-block';
}

function displayTeams(teams) {
  const teamsDiv = document.getElementById('teams');
  teamsDiv.innerHTML = '';

  teams.forEach((team, index) => {
    const teamDiv = document.createElement('div');
    teamDiv.className = 'team';
    teamDiv.innerHTML = `<h3>Team ${index + 1}</h3>`;

    team.forEach((member) => {
      const avatar = document.createElement('div');
      avatar.className = 'avatar';
      avatar.textContent = member;
      teamDiv.appendChild(avatar);
    });

    teamsDiv.appendChild(teamDiv);
  });
}

function displayCountdownWindow() {
  const newWindow = window.open('', 'Countdown Window', 'width=800,height=600');

  const doc = newWindow.document;
  doc.open();
  doc.write(`
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Countdown</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; }
                .countdown { font-size: 20px; font-weight: bold; }
                @keyframes flashBg { 0% { background-color: red; } 100% { background-color: yellow; } }
            </style>
            <script>
                function startCountdown(member) {
                    const timer = document.getElementById('timer-' + member);
                    let timeLeft = 60;

                    const interval = setInterval(() => {
                        timeLeft--;
                        const minutes = Math.floor(timeLeft / 60);
                        const seconds = timeLeft % 60;
                        timer.textContent = minutes + ':' + (seconds < 10 ? '0' + seconds : seconds);

                        if (timeLeft <= 0) {
                            clearInterval(interval);
                            timer.textContent = 'Time is up!';
                        }
                    }, 1000);
                }
            </script>
        </head>
        <body>
            <h1>Teams</h1>
            ${currentTeams
              .map(
                (team, index) =>
                  `<h2>Team ${index + 1}</h2>` +
                  team
                    .map(
                      (member) => `
                        <div>
                            <p>${member}</p>
                            <button onclick="startCountdown('${member}')">Start Timer</button>
                            <div id="timer-${member}" class="countdown">1:00</div>
                        </div>`
                    )
                    .join('')
              )
              .join('')}
        </body>
        </html>
    `);
  doc.close();
}
