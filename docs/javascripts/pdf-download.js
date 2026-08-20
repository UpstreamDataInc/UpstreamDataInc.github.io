(() => {
  "use strict";

  const ENGINE_FILES = new Map([
    ["5.7L GM", "5-7l-gm.pdf"],
    ["6.7LT PSI", "6-7lt-psi.pdf"],
    ["11LT PSI", "11lt-psi.pdf"],
    ["13LT PSI", "13lt-psi.pdf"],
    ["22LT Mesa", "22lt-mesa.pdf"],
  ]);

  function selectedEngine(article) {
    const tabSet = article.querySelector(".tabbed-set");
    if (!tabSet) return null;

    const inputs = Array.from(
      tabSet.querySelectorAll(":scope > input[type='radio']"),
    );
    const selectedIndex = Math.max(
      0,
      inputs.findIndex((input) => input.checked),
    );
    const labels = tabSet.querySelectorAll(
      ":scope > .tabbed-labels > label",
    );
    return labels[selectedIndex]?.textContent.trim() || null;
  }

  function updateDownloadLink(link, article) {
    const engine = selectedEngine(article);
    const filename = ENGINE_FILES.get(engine);
    if (!filename) {
      link.hidden = true;
      return;
    }

    link.href = new URL(
      `../downloads/maintenance/${filename}`,
      window.location.href,
    ).href;
    link.download = `maintenance-${filename}`;
    link.textContent = `Download ${engine} PDF`;
    link.hidden = false;
  }

  function installPdfLink() {
    const path = window.location.pathname
      .replace(/index\.html$/, "")
      .replace(/\/+$/, "");
    const article = document.querySelector(".md-content__inner");

    if (!path.endsWith("/maintenance") || !article) return;

    let link = article.querySelector(".pdf-download");
    if (!link) {
      link = document.createElement("a");
      link.className = "md-button pdf-download";
      article.prepend(link);

      article
        .querySelectorAll(".tabbed-set > input[type='radio']")
        .forEach((input) => {
          input.addEventListener("change", () => {
            updateDownloadLink(link, article);
          });
        });
    }

    updateDownloadLink(link, article);
  }

  if (typeof window.document$ !== "undefined") {
    window.document$.subscribe(installPdfLink);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", installPdfLink);
  } else {
    installPdfLink();
  }
})();
