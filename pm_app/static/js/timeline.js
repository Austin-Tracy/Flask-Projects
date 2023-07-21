// app/static/js/timeline.js
function generateTimeline(tasks) {
    console.log("Timeline script is running");
    let timeline = document.getElementById("timeline");
    let sortedTasks = tasks.sort((a, b) => new Date(a.deadline) - new Date(b.deadline));
  
    sortedTasks.forEach((task, index) => {
      let container = document.createElement("div");
      container.classList.add("container-timeline");
      container.innerHTML = `
        <a href="${task.url}" class="text-decoration-none">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">${task.title}</h5>
              <p class="card-text">${task.description}</p>
              <p class="card-text"><small class="text-muted">${task.deadline}</small></p>
            </div>
          </div>
        </a>
      `;
  
      let position = document.createElement("div");
      position.classList.add(index % 2 === 0 ? "left-timeline" : "right-timeline");
      position.appendChild(container);
  
      timeline.appendChild(position);
    });
  }