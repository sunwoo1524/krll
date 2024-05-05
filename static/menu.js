const menu_btn = document.getElementById("menu-btn");
const menu = document.getElementById("menu");

menu_btn.onclick = () => {
    menu.classList.toggle("show");
}

window.onclick = e => {
    if (!e.target.matches(".menu-btn")) {
        if (menu.classList.contains("show")) {
            menu.classList.remove("show");
        }
    }
}