console.log("✅ ToxiShield script injected");

const API_URL = "https://vishakhast-toxishield1.hf.space/api/predict";

async function analyzeComment(text, element) {
  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ text: text })
    });

    const data = await response.json();

    if (!data || !data.label) return;

    // 🔥 NEW: send data to admin backend (does NOT affect existing logic)
    fetch("http://127.0.0.1:5001/save", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        text: text,
        label: data.label,
        platform: window.location.hostname
      })
    }).catch(err => console.log("Admin save failed:", err));

    // Existing logic (UNCHANGED)
    if (data.label === "toxic") {
      applyToxicUI(element, data.toxicity_percent, data.toxicity_level);
    }

  } catch (error) {
    console.error("Error:", error);
  }
}

function applyToxicUI(element, percent, level) {
  if (element.dataset.toxishieldApplied) return;
  element.dataset.toxishieldApplied = "true";

  let isHidden = true;

  // Blur
  element.style.filter = "blur(6px)";
  element.style.transition = "0.2s ease";

  const container =
    element.closest("ul li") ||
    element.closest("div[role='button']") ||
    element.parentElement;

  if (!container) return;

  container.style.position = "relative";

  // 🔴 BUTTON (BOTTOM RIGHT)
  const btn = document.createElement("button");
  btn.innerText = "View";

  btn.style.position = "absolute";
  btn.style.bottom = "2px";
  btn.style.right = "2px";

  btn.style.padding = "4px 10px";
  btn.style.fontSize = "11px";
  btn.style.border = "none";
  btn.style.borderRadius = "8px";
  btn.style.cursor = "pointer";
  btn.style.background = "#ef4444";
  btn.style.color = "#fff";
  btn.style.zIndex = "10";

  container.appendChild(btn);

  // 🔵 TOXICITY INFO (BOTTOM LEFT)
  const info = document.createElement("div");
  info.innerText = `${percent}% • ${level}`;

  info.style.position = "absolute";
  info.style.bottom = "4px";
  info.style.left = "4px";

  info.style.fontSize = "11px";
  info.style.padding = "2px 6px";
  info.style.borderRadius = "6px";
  info.style.background = "rgba(0,0,0,0.6)";
  info.style.color = "#fff";
  info.style.zIndex = "10";

  container.appendChild(info);

  // 🔥 TOOLTIP
  const tooltip = document.createElement("div");
  tooltip.innerText = "⚠ Toxic comment detected";

  tooltip.style.position = "absolute";
  tooltip.style.bottom = "30px";
  tooltip.style.left = "0";

  tooltip.style.background = "rgba(0,0,0,0.85)";
  tooltip.style.color = "#fff";
  tooltip.style.fontSize = "11px";
  tooltip.style.padding = "4px 8px";
  tooltip.style.borderRadius = "6px";
  tooltip.style.whiteSpace = "nowrap";
  tooltip.style.opacity = "0";
  tooltip.style.pointerEvents = "none";
  tooltip.style.transition = "0.2s";
  tooltip.style.zIndex = "10";

  container.appendChild(tooltip);

  // Hover ONLY on text
  element.addEventListener("mouseenter", () => {
    tooltip.style.opacity = "1";
  });

  element.addEventListener("mouseleave", () => {
    tooltip.style.opacity = "0";
  });

  // Toggle
  btn.onclick = () => {
    isHidden = !isHidden;

    if (isHidden) {
      element.style.filter = "blur(6px)";
      btn.innerText = "View";
      btn.style.background = "#ef4444";
    } else {
      element.style.filter = "none";
      btn.innerText = "Hide";
      btn.style.background = "#3b82f6";
    }
  };
}

function scanComments() {
  const comments = document.querySelectorAll("span");

  comments.forEach(el => {
    const text = el.innerText;

    if (
      text &&
      text.length > 5 &&
      !el.dataset.toxishieldChecked
    ) {
      el.dataset.toxishieldChecked = "true";
      analyzeComment(text, el);
    }
  });
}

setInterval(scanComments, 1500);
