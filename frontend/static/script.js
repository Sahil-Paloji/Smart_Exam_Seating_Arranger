const subjectFields = document.getElementById("subjectFields");
const gridSizeInput = document.getElementById("gridSize");
const subjectCountInput = document.getElementById("subjectCount");
const message = document.getElementById("message");
const resultSection = document.getElementById("resultSection");
const grid = document.getElementById("grid");
const legend = document.getElementById("legend");
const resultSummary = document.getElementById("resultSummary");

const defaults = [
  ["DAA", 4],
  ["DBMS", 4],
  ["SM", 4],
  ["ES", 4],
];

function createSubjectFields() {
  let count = Math.max(1, Math.min(10, Number(subjectCountInput.value) || 1));
  subjectCountInput.value = count;
  subjectFields.innerHTML = "";

  for (let i = 0; i < count; i++) {
    const d = defaults[i] || [`Subject ${i + 1}`, 1];
    const row = document.createElement("div");
    row.className = "subject-row";
    row.innerHTML = `
            <div class="subject-number">${i + 1}</div>
            <label>Subject Name
                <input class="subject-name" type="text" value="${escapeHtml(d[0])}">
            </label>
            <label>Students
                <input class="student-count" type="number" min="0" value="${d[1]}">
            </label>
        `;
    subjectFields.appendChild(row);
  }
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function showMessage(text, type = "") {
  message.textContent = text;
  message.className = `message ${type}`;
}

async function generateSeating() {
  showMessage("Generating arrangement...");

  const subjects = [...document.querySelectorAll(".subject-row")].map(
    (row) => ({
      name: row.querySelector(".subject-name").value.trim(),
      students: Number(row.querySelector(".student-count").value),
    }),
  );

  try {
    const response = await fetch("/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        gridSize: Number(gridSizeInput.value),
        subjects,
      }),
    });

    const data = await response.json();

    if (!data.success) {
      resultSection.classList.add("hidden");
      showMessage(data.message, "error");
      return;
    }

    renderResult(data, Number(gridSizeInput.value));
    showMessage("Valid seating arrangement generated.", "success");
  } catch {
    resultSection.classList.add("hidden");
    showMessage("Could not connect to the backend.", "error");
  }
}

function renderResult(data, n) {
  resultSection.classList.remove("hidden");

  grid.style.gridTemplateColumns = `repeat(${n}, 1fr)`;
  grid.innerHTML = "";

  data.grid.flat().forEach((id) => {
    const seat = document.createElement("div");
    seat.className = "seat";

    if (id === 0) {
      seat.textContent = "EMPTY";
      seat.classList.add("empty-seat");
    } else {
      const subject = data.subjects[id - 1];

      if (!subject) {
        throw new Error(`Invalid subject ID: ${id}`);
      }

      seat.textContent = subject.code;
      seat.title = subject.name;
    }

    grid.appendChild(seat);
  });

  legend.innerHTML = "";

  data.subjects.forEach((s) => {
    const item = document.createElement("div");
    item.className = "legend-item";
    item.textContent = `${s.code} = ${s.name} (${s.students})`;

    legend.appendChild(item);
  });

  const total = data.subjects.reduce((sum, s) => sum + s.students, 0);

  resultSummary.textContent = `${n} × ${n} grid • ${total} students • ${data.subjects.length} subjects`;
}

document
  .getElementById("createSubjects")
  .addEventListener("click", createSubjectFields);
document.getElementById("generate").addEventListener("click", generateSeating);

createSubjectFields();
