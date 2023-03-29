'use strict;'

const search = document.getElementById('searchbarEp');

search.addEventListener('keyup', e=>{
    if(e.key == "ESC")
        return;

    input = e.target.value.toLowerCase();

    const episodes = document.getElementsByClassName('episodio');                //prendo tutte le classi che rappresentano il singolo episodio
    console.log(episodes);

    //Controllo uguaglianza ricerca
    for (let episode of episodes){
        let title = episode.querySelector('.titoloEp').innerText;
        let descr = episode.querySelector('.descrEp').innerText;
        console.log(title);
        console.log(descr)
        if (title.toLowerCase().indexOf(input) == -1 && descr.toLowerCase().indexOf(input) == -1){          
            episode.classList.add('hide');
        }
        else
            episode.classList.remove('hide');
    }
    }
);
