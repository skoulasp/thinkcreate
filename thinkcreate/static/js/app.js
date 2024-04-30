const searchMagnifier = document.querySelector("#search-btn");
const mainHeader = document.querySelector(".main-header");
const searchBar = document.querySelector("#search");
const navItems = document.querySelector(".dynamic");
let errorWarning = document.querySelector(".message");
const container = document.querySelector(".container");
const modal = document.querySelector(".modal");
const dropdown = document.querySelector(".dd-button");
const dropdownMobile = document.querySelector(".mobile-dropdown-button");
const dropdownNavMobile = document.querySelector(".nav-dropdown-button");
let inputText;
let isSearchBarOpen = false;
document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && isSearchBarOpen) {
        searchBarClose();
    }
});

document.addEventListener("click", (e) => {
    if (e.target.closest(".x-remove")) {
        document.querySelector("div.message").remove();
    }
    if (searchMagnifier && !isSearchBarOpen && e.target.closest("#search-btn")) {
        searchBarOpen();
    } else if (
        isSearchBarOpen &&
        e.target !== searchMagnifier &&
        e.target !== searchMagnifier.firstChild &&
        e.target !== searchBar.children[0].children[0]
    ) {
        searchBarClose();
    }
});

if (searchBar) {
    searchBar.children[0].classList.add("invisible");
    let xclose = searchBar.children[2];
}

const searchBarOpen = () => {
    if (isSearchBarOpen) return;
    isSearchBarOpen = true;
    searchMagnifier.firstChild.classList.remove("zoomIn");
    searchMagnifier.firstChild.classList.add("zoomOut");
    searchMagnifier.firstChild.classList.add("invisible");
    searchBar.children[2].firstChild.classList.remove("invisible");
    searchBar.children[2].firstChild.classList.remove("zoomOut");
    searchBar.children[2].firstChild.classList.add("zoomIn");
    searchBar.children[0].classList.remove("invisible");
    searchBar.children[0].children[0].classList.add("search-box", "zoomInRight");
    navItems.classList.add("slideInRight");
    searchBar.children[2].classList.remove("invisible");
    searchBar.children[0].children[0].focus();
    modal.classList.add("dim");
};

const searchBarClose = () => {
    isSearchBarOpen = false;
    modal.classList.remove("dim");
    searchMagnifier.firstChild.classList.remove("zoomOut");
    searchMagnifier.firstChild.classList.add("zoomIn");
    searchBar.children[2].firstChild.classList.remove("zoomIn");
    searchBar.children[2].firstChild.classList.add("zoomOut");
    searchBar.children[2].firstChild.classList.add("invisible");
    navItems.classList.remove("slideInRight");
    searchMagnifier.firstChild.classList.remove("invisible");
    navItems.classList.add("slideInLeft");
    searchBar.children[0].classList.add("invisible");
    searchMagnifier.classList.remove("invisible");
    if (!searchMagnifier.firstChild.classList.contains("zoomIn") && searchBar.children[0].children[0].classList.contains("search-box")) {
        searchMagnifier.firstChild.classList.add("zoomIn");
    }

    searchBar.children[0].children[0].value = "";
};

if (searchBar) {
    searchBar.children[0].children[0].addEventListener("keydown", (e) => {
        if (e.target.value !== "") {
            inputText = e.target.value;
        }
    });
}

document.addEventListener("click", (e) => {
    if (e.target.classList.contains("x-remove")) {
        e.target.classList.add("fadeOut");
        setTimeout(function () {
            e.target.parentElement.remove();
        }, 400);
        e.target.classList.remove("fadeOut");
    }
});

document.addEventListener("click", (e) => {
    if (e.target.closest("#search-btn")) return;

    if (e.target == dropdown && !dropdown.children[0].classList.contains("drop") && dropdown !== null) {
        dropdown.children[0].classList.remove("fadeOut");
        dropdown.children[0].classList.add("drop");
        dropdown.children[0].classList.add("bounceIn");
    } else if (dropdown !== null && dropdown !== undefined) {
        dropdown.children[0].classList.add("fadeOut");
        dropdown.children[0].classList.remove("drop");
        dropdown.children[0].classList.remove("bounceIn");
    }

    if (
        e.target.className == "mobile-dropdown" &&
        !dropdownMobile.children[0].classList.contains("drop") &&
        dropdownMobile.children[0] !== null
    ) {
        dropdownMobile.classList.remove("fadeInDown");
        dropdownMobile.children[0].classList.add("drop");
        dropdownMobile.classList.add("fadeInDown");
    } else {
        dropdownMobile.classList.add("fadeInDown");
        dropdownMobile.children[0].classList.remove("drop");
        dropdownMobile.classList.remove("fadeInDown");
    }

    if (
        e.target.className == "nav-dropdown" &&
        !dropdownNavMobile.children[0].classList.contains("drop") &&
        dropdownNavMobile.children[0] !== null
    ) {
        dropdownNavMobile.classList.remove("fadeInDown");
        dropdownNavMobile.children[0].classList.add("drop");
        dropdownNavMobile.classList.add("fadeInDown");
    } else {
        dropdownNavMobile.classList.add("fadeInDown");
        if (e.target.className != "search-form-mobile") {
            dropdownNavMobile.children[0].classList.remove("drop");
        }
        dropdownNavMobile.classList.remove("fadeInDown");
    }
});

const viewportHeight = window.innerHeight;
const viewportWidth = window.innerWidth;
const offsetHeight = document.querySelector("html").offsetHeight;
const footerExists = document.querySelector(".footer");

window.onload = function () {
    if (footerExists) {
        let footerHeight = footerExists.scrollHeight;
        container.style.cssText = "padding-bottom: calc(" + footerHeight + "px + 60px);";
    }
};
