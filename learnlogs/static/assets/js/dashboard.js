// add hovered class to selected list item
let list = document.querySelectorAll(".navigation li");

function activeLink() {
  list.forEach((item) => {
    item.classList.remove("hovered");
  });
  this.classList.add("hovered");
}

list.forEach((item) => item.addEventListener("mouseover", activeLink));

// Menu Toggle
let toggle = document.querySelector(".toggle");
let navigation = document.querySelector(".navigation");
let main = document.querySelector(".main");

toggle.onclick = function () {
  navigation.classList.toggle("active");
  main.classList.toggle("active");
};
document.addEventListener('DOMContentLoaded', function() {
  const gradeLinks = document.querySelectorAll('.grade-link');

  gradeLinks.forEach(link => {
      link.addEventListener('click', function() {
          const grade = this.getAttribute('data-grade');
          const gradeIcon = document.querySelector(`.grade-icon[data-grade="${grade}"] ion-icon`);

          const hiddenItems = document.querySelectorAll(`.${grade}-grade`);

          hiddenItems.forEach(item => {
              item.classList.toggle('hidden');
          });

          // Toggle icon
          if (gradeIcon.getAttribute('name') === 'caret-down-outline') {
              gradeIcon.setAttribute('name', 'caret-up-outline');
          } else {
              gradeIcon.setAttribute('name', 'caret-down-outline');
          }
      });
  });
});