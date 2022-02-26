const  popupLinks = document.querySelectorAll('.popup-link');
const  body = document.getElementById('body');
const  lockPadding = document.querySelectorAll(".lock-padding");
const openPopUp = document.getElementById('open_pop_up');
const closePopUp = document.getElementById('pop_up_close');
const PopUp = document.getElementById('popup-block');




let unlock = true;

const timeout = 800;

if(popupLinks.length > 0){
    for(let index = 0; index < popupLinks.length;index++){
        const popupLink = popupLinks[index];

        popupLink.addEventListener("click",function(e){
            const popupName = popupLink.getAttribute('href').replace('#','');
            const curentPopup = document.getElementById(popupName);
            popupOpen(curentPopup);
            e.preventDefault();
        });
    }
}

const popupCloseIcon = document.querySelectorAll('.popup-block-close');
if(popupCloseIcon.length > 0){
    for(let index = 0; index < popupCloseIcon.length;index++)
        {
            const el = popupCloseIcon[index];
            el.addEventListener('click',function(e){
                popupClose(el.closest('.popup-block'));
                e.preventDefault();
            });
        }
}

function popupOpen(curentPopup){
    if(curentPopup && unlock){
        const popupActive = openPopUp;
        if(popupActive){
            popupClose(popupActive,false);
        }else{
            body.classList.add('lock');
        }
        curentPopup.classList.add('active');
        body.classList.add('lock');
        curentPopup.addEventListener("click",function(e){
            if(!e.target.closest('.popup-block-content')){
                popupClose(e.target.closest(PopUp));
            }
        });
    }
}

function popupClose(popupActive,doUnlock = true){
    if(unlock){
        popupActive.classList.remove('active');
        if(doUnlock){
            bodyUnlock();
        }
    }
}

function bodyLock(){
    const lockPaddingValue = window.innerWidth - document.querySelector('.wrapper1').offsetWidth + 'px';
    if(lockPadding.length > 0){
        for(let index = 0; index < lockPadding.length;index++){
        const el = lockPadding[index];
        el.style.paddingRight = lockPaddingValue;
        }
    }

    body.style.paddingRight = lockPaddingValue;
    body.classList.add('lock');

    unlock = false;
    setTimeout(function(){
        unlock = true;
    },timeout);
}

function bodyUnlock(){
    setTimeout(function(){
        if(lockPadding.length > 0){
        for(let index = 0; index < lockPadding.length;index++){
            const el = lockPadding[index];
            el.style.paddingRight = '0px';
        }
    }
        body.style.paddingRight = '0px';
        body.classList.remove('lock');
    },timeout);

    unlock = false;
    setTimeout(function(){
        unlock = true;
    },timeout);

}


document.addEventListener('keydown',function(e){
    if(e.which === 27){
        const popupActive = document.querySelector('.popup-block.open');
        popupClose(popupActive);
    }
});

(function(){
    if(!Element.prototype.closest){
        Element.prototype.closest = function(css){
            var node = this;
            while(node){
                if(node.matches(css)) return node;
                else node = node.parentElement;
            }
            return null;
        }
    }
})();
(function(){
    if(!Element.prototype.matches){
        Element.prototype.matches = Element.prototype.matchesSelector ||
            Element.prototype.webkitMatchesSelector ||
            Element.prototype.mozMatchesSelector ||
            Element.prototype.msMatchesSelector;
    }
})();
