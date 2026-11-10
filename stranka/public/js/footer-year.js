(() => {
  const updateYear = () => {
    const year = document.getElementById('tesla-current-year');
    if (year) year.textContent = new Date().getFullYear();
  };

  updateYear();
  // Aktualizuje aj stránku ponechanú otvorenú cez koniec roka.
  setInterval(updateYear, 60 * 60 * 1000);
  document.addEventListener('visibilitychange', updateYear);
})();
