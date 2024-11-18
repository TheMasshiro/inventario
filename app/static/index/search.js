function initSearch(type) {
  const searchInput = document.getElementById(`${type}-search-input`);
  const tbody = document.getElementById(`${type}s-tbody`);

  if (!searchInput || !tbody) return;

  let timeoutId;

  searchInput.addEventListener("input", function () {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(async function () {
      try {
        const response = await fetch(`/${type}/search?q=${searchInput.value}`);
        if (!response.ok) throw new Error(`${type} search failed`);

        const html = await response.text();
        tbody.innerHTML = html;
        initModals();
      } catch (error) {
        console.error(`Error searching ${type}s:`, error);
      }
    }, 300);
  });
}
