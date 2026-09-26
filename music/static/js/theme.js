

// Each theme has:
// an id: used by CSS and JavaScript
// a label: shown on the theme button
const themes = [
    {
        id: "white-gold",
        label: "WHITE GOLD"
    },
    {
        id: "red-teal",
        label: "RED & TEAL"
    },
    {
        id: "dark-blue",
        label: "DARK BLUE"
    }
];



// Get the theme currently stored on the <html> element.
// <html data-theme="red-teal"> will return "red-teal".
// The cream theme is the default theme
function getCurrentTheme() {
    const currentTheme =
        document.documentElement.dataset.theme;
    if (currentTheme) {
        return currentTheme;
    }
    return "white-gold";
}




// Change the theme of the website
// Cream is the default theme, so remove data-theme when cream is selected
// For other themes, add data-theme to <html>
function applyTheme(themeId) {
    const html = document.documentElement;

    if (themeId === "white-gold") {
        // White-gold is the default theme.
        html.removeAttribute("data-theme");

    } else {
        // Other themes use the data-theme attribute.
        html.dataset.theme = themeId;
    }

    // Save the selected theme in localStorage
    // theme can be remembered when the user visits the page again
    localStorage.setItem(
        "app_theme",
        themeId
    );

    // Update the text displayed on the theme button
    updateThemeButton(themeId);
}





//  Change the button text to show the current theme.
function updateThemeButton(themeId) {

    const button =
        document.getElementById("theme-button");

    // Stop if the button does not exist on this page.
    if (!button) {
        return;
    }

    // Find the theme with the same id
    const theme =
        themes.find(function(theme) {
            return theme.id === themeId;
        });

    // Stop if the theme cannot be found.
    if (!theme) {
        return;
    }

    // Show the theme name on the button.
    button.textContent = theme.label;
}




//  When the user clicks the theme button, change to the next theme.
//  order: White Gold - Red & Teal - Dark Blue
function cycleTheme() {

    // Get the theme currently being used.
    const currentTheme = getCurrentTheme();

    // Find the position of the current theme in the themes array.
    const currentIndex =
        themes.findIndex(function(theme) {
            return theme.id === currentTheme;
        });

    // Move to the next theme.
    // loop back to the first theme after the last one
    let nextIndex = currentIndex + 1;
    if (nextIndex >= themes.length) {
        nextIndex = 0;
    }

    // Get the next theme from the array.
    const nextTheme = themes[nextIndex];

    // Apply the new theme.
    applyTheme(nextTheme.id);
}



//  Wait until the HTML page has loaded.
document.addEventListener(
    "DOMContentLoaded",
    function() {


        //  Get the theme saved in localStorage.
        let savedTheme =
            localStorage.getItem("app_theme");
        if (!savedTheme) {
        savedTheme = "white-gold";
        }

        //  Check the saved theme
        let validTheme = false;
        for (let i = 0; i < themes.length; i++) {
            if (themes[i].id === savedTheme) {
                validTheme = true;
                break;
            }
        }

        // If the saved theme is invalid,
        //  use the default white-gold theme.
        if (!validTheme) {
            savedTheme = "white-gold";
        }

        // Apply the saved theme when the page loads.
        applyTheme(savedTheme);
    }
);