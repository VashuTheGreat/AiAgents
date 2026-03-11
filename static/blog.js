/* ============================================================
   blog.js  –  Blog page logic.
   Requires: constants.js (loaded before this script)
   ============================================================ */

// ── State ─────────────────────────────────────────────────
let currentBlogData = null;
let isGenerating = false;

// ── Initialize marked and highlight.js ───────────────────
marked.setOptions({
  highlight: function (code, lang) {
    if (lang && hljs.getLanguage(lang)) {
      return hljs.highlight(code, { language: lang }).value;
    }
    return hljs.highlightAuto(code).value;
  },
  breaks: true,
});

// ── History ───────────────────────────────────────────────
async function loadHistory() {
  const res = await fetch(ROUTES.BLOGS_LIST, {
    headers: AUTH_HEADERS(),
  });
  const blogs = await res.json();
  const container = document.getElementById("history-container");
  container.innerHTML = "";

  blogs.forEach((title) => {
    const div = document.createElement("div");
    div.className = "history-item";
    div.textContent = title;
    div.onclick = () => loadBlog(title);
    container.appendChild(div);
  });
}

async function loadBlog(title) {
  if (isGenerating) return;

  const res = await fetch(ROUTES.BLOG_GET(title), {
    headers: AUTH_HEADERS(),
  });
  if (!res.ok) return;

  const data = await res.json();
  currentBlogData = {
    topic: title,
    plan: { blog_title: title },
    final: data.content,
  };

  displayBlog(data.content);
  document.getElementById("blog-title-display").textContent = title;

  // Mark as active in sidebar
  document.querySelectorAll(".history-item").forEach((item) => {
    item.classList.toggle("active", item.textContent === title);
  });

  // Enable actions
  document.getElementById("download-btn").disabled = false;
  document.getElementById("delete-btn").disabled = false;
}

// ── Display ───────────────────────────────────────────────
function displayBlog(markdown) {
  const blogContent = document.getElementById("blog-content");
  const welcome = document.getElementById("welcome-screen");
  const pipeline = document.getElementById("pipeline-status");

  welcome.style.display = "none";
  pipeline.style.display = "none";
  blogContent.style.display = "block";

  // Rewrite image paths to use the /blog/images static mount if they are internal
  const processedMd = markdown.replace(/\(\.\.\/images\//g, "(/blog/images/");

  blogContent.innerHTML = marked.parse(processedMd);
  hljs.highlightAll();
}

function startNewBlog() {
  if (isGenerating) return;

  currentBlogData = null;
  document.getElementById("welcome-screen").style.display = "flex";
  document.getElementById("blog-content").style.display = "none";
  document.getElementById("pipeline-status").style.display = "none";
  document.getElementById("blog-title-display").textContent = "Blog Overview";
  document.getElementById("topic-input").value = "";
  document.getElementById("download-btn").disabled = true;
  document.getElementById("delete-btn").disabled = true;

  document.querySelectorAll(".history-item").forEach((item) => {
    item.classList.remove("active");
  });
}

function appendStatus(msg) {
  const pipeline = document.getElementById("pipeline-status");
  pipeline.style.display = "block";
  const line = document.createElement("div");
  line.className = "status-line";
  line.innerHTML = `<span style="color: #6ee7b7;">[${new Date().toLocaleTimeString()}]</span> ${msg}`;
  pipeline.appendChild(line);
  pipeline.scrollTop = pipeline.scrollHeight;
}

// ── Generation ────────────────────────────────────────────
function startGeneration() {
  const topicInput = document.getElementById("topic-input");
  const topic = topicInput.value.trim();
  if (!topic || isGenerating) return;

  isGenerating = true;
  setLoading(true);

  document.getElementById("welcome-screen").style.display = "none";
  document.getElementById("blog-content").style.display = "none";
  const pipeline = document.getElementById("pipeline-status");
  pipeline.innerHTML = "";
  pipeline.style.display = "block";

  appendStatus(`Initializing generation for topic: "${topic}"...`);

  // WebSocket – pass user_id as a query param since WS doesn't support custom headers
  const wsUrl = new URL(ROUTES.BLOG_WS());
  wsUrl.searchParams.set("user_id", getUserId());
  const ws = new WebSocket(wsUrl.toString());

  ws.onopen = () => {
    ws.send(JSON.stringify({ topic }));
  };

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);

    if (data.status === "completed") {
      appendStatus("Done! Finalizing blog post...");
    } else if (data.final) {
      currentBlogData = data;
      displayBlog(data.final);
      loadHistory();
      setLoading(false);
      isGenerating = false;
      document.getElementById("download-btn").disabled = false;
      document.getElementById("delete-btn").disabled = false;
      if (data.plan && data.plan.blog_title) {
        document.getElementById("blog-title-display").textContent =
          data.plan.blog_title;
      }
    } else if (data.error) {
      appendStatus(`<span style="color: #f87171;">ERROR: ${data.error}</span>`);
      setLoading(false);
      isGenerating = false;
    } else {
      if (data.sections && data.sections.length > 0) {
        const lastSection = data.sections[data.sections.length - 1];
        appendStatus(
          `Generated section: ${lastSection[1].split("\n")[0].replace("## ", "")}`
        );
      } else if (data.plan) {
        appendStatus(
          `Plan created: "${data.plan.blog_title}" with ${data.plan.tasks.length} sections.`
        );
      } else if (data.queries && data.queries.length > 0) {
        appendStatus(`Researching: ${data.queries.join(", ")}`);
      }
    }
  };

  ws.onerror = () => {
    appendStatus(`<span style="color: #f87171;">Connection error.</span>`);
    setLoading(false);
    isGenerating = false;
  };

  ws.onclose = () => {
    if (isGenerating) {
      appendStatus("Connection closed.");
      setLoading(false);
      isGenerating = false;
    }
  };
}

function setLoading(loading) {
  const btn = document.getElementById("generate-btn");
  if (loading) {
    btn.disabled = true;
    btn.innerHTML = '<div class="spinner"></div>';
  } else {
    btn.disabled = false;
    btn.innerHTML = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"/><polyline points="22 2 15 22 11 13 2 9 22 2"/></svg>`;
  }
}

// ── CRUD Actions ──────────────────────────────────────────
async function deleteCurrentBlog() {
  if (
    !currentBlogData ||
    !confirm("Are you sure you want to delete this blog and all related images?")
  )
    return;

  const res = await fetch(ROUTES.BLOG_DELETE, {
    method: "DELETE",
    headers: AUTH_HEADERS(),
    body: JSON.stringify({ data: currentBlogData }),
  });

  if (res.ok) {
    startNewBlog();
    loadHistory();
  } else {
    alert("Failed to delete blog.");
  }
}

function downloadCurrentBlog() {
  if (!currentBlogData) return;
  const title = currentBlogData.plan
    ? currentBlogData.plan.blog_title
    : currentBlogData.topic;
  window.location.href = ROUTES.BLOG_DOWNLOAD(title);
}

// ── Bootstrap ─────────────────────────────────────────────
loadHistory();
