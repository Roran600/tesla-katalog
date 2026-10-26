// Apply the selected theme before first paint to prevent a color flash.
function setTheme(theme) {
  document.documentElement.classList.remove("light", "dark", "gray");

  if (theme !== "light" && theme !== "dark" && theme !== "gray") {
    theme = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }

  if (theme === "gray") {
    document.documentElement.classList.add("dark", "gray");
    document.documentElement.style.colorScheme = "dark";
  } else {
    document.documentElement.classList.add(theme);
    document.documentElement.style.colorScheme = theme;
  }
}

setTheme("color-theme" in localStorage ? localStorage.getItem("color-theme") : '{{ site.Params.theme.default | default `system`}}')
