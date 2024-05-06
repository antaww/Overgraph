// Hero data
const heroes = ['Ana', 'Ange', 'Ashe', 'Baptiste', 'Bastion', 'Bouldozer', 'Brigitte', 'D.Va', 'Doomfist', 'Echo', 'Genji', 'Hanzo', 'Chacal', 'Lúcio', 'Cassidy', 'Mei', 'Orisa','Moira', 'Pharah', 'Reaper', 'Reinhardt', 'Roadhog', 'Sigma', 'Soldat', 'Sombra', 'Symmetra', 'Torbjörn', 'Tracer', 'fatale', 'Winston', 'Zarya', 'Zenyatta']

const images = ['chara_img/ana.png', 'chara_img/ange.png', 'chara_img/ashe.png', 'chara_img/baptiste.png', 'chara_img/bastion.png', 'chara_img/bouldozer.png', 'chara_img/brigitte.png', 'chara_img/dva.png', 'chara_img/doomfist.png', 'chara_img/echo.png', 'chara_img/genji.png', 'chara_img/hanzo.png', 'chara_img/chacal.png', 'chara_img/lucio.png', 'chara_img/cassidy.png','chara_img/mei.png', 'chara_img/orisa.png', 'chara_img/moira.png', 'chara_img/pharah.png', 'chara_img/faucheur.png', 'chara_img/reinhardt.png', 'chara_img/chopper.png', 'chara_img/sugma.png', 'chara_img/soldat.png', 'chara_img/sombra.png', 'chara_img/symmetra.png', 'chara_img/torbjorn.png', 'chara_img/tracer.png', 'chara_img/fatale.png', 'chara_img/winston.png', 'chara_img/zarya.png', 'chara_img/zenyatta.png']

document.addEventListener('DOMContentLoaded', () => {

  // Select container
  const container = document.getElementById('checkboxes');

  // Loop heroes
  heroes.forEach((hero, i) => {

    // Create elements
    const checkbox = document.createElement('input');
    const label = document.createElement('label');
    const img = document.createElement('img');

    // Set attributes & text
    checkbox.type = 'checkbox';
    label.innerHTML = hero;
    img.src = images[i];

    // Add classes
    checkbox.classList.add('hero');
    label.classList.add('label');
    img.classList.add('image');

    // Append to container
    container.append(checkbox);
    container.append(label);
    container.append(img);

  });

  // Checkbox handler
  const checkboxes = document.querySelectorAll('.hero');

  checkboxes.forEach(checkbox => {

    checkbox.addEventListener('change', () => {

      // when i check an img it will be grayscale
        const img = checkbox.nextElementSibling.nextElementSibling;
        if (checkbox.checked) {
          img.style.filter = 'grayscale(100%)';
        } else {
          img.style.filter = 'grayscale(0%)';
        }
    });

  });

});

