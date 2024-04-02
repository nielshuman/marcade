const PACMAN_DURATION = 14000;
const MARIO_DURATION = 5000;
const KITTY_DURATION = 5000;

function animatePacman() {
    path = document.getElementById('pacman');
    path.classList.add('final__path');
    path.innerHTML = `
    <div class="block"></div>
    <div class="final__pacman"></div>
    <div class="final__ghost">
      <div class="final__eyes"></div>
      <div class="final__skirt"></div>
    </div>
    `
    setTimeout(() => {
        path.classList.remove('final__path');
        path.innerHTML = '';
    }, PACMAN_DURATION);
}

const mario = document.getElementById('mario');
function animateMario() {
    mario.classList.add('animate-mario');
    setTimeout(() => {
        mario.classList.remove('animate-mario');
    }, MARIO_DURATION);
}

const kitty = document.getElementById('kitty')
function animateKitty() {
    kitty.classList.add('animate-kitty');
    setTimeout(() => {
        kitty.classList.remove('animate-kitty');
    }, KITTY_DURATION);
}