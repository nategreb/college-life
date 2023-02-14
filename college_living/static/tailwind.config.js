/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "../templates/**/*.{html,js}",
        './node_modules/flowbite/**/*.js'
    ], //parse content in these locations
    theme: {
        extend: {},
    },
    plugins: [
        require('flowbite/plugin')
    ],
}