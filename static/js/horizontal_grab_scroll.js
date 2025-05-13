/* 
  this is an implementation of Wes Bos click & drag scroll algorythm. In his video, he shows how to do the horizontal scroll. I have implemented the vertical scroll for those wondering how to make it as well.
  
  Wes Bos video:
    https://www.youtube.com/watch?v=C9EWifQ5xqA
*/
const container = document.querySelectorAll('#container-horizontal-scrolled');
                
let startY;
let startX;
let scrollLeft;
let scrollTop;
let isDown;

for(let index=0;index<container.length;index++){
  container[index].addEventListener('mousedown',e => mouseIsDown(e, index));  
  container[index].addEventListener('mouseup',e => mouseUp(e))
  container[index].addEventListener('mouseleave',e=>mouseLeave(e));
  container[index].addEventListener('mousemove',e=>mouseMove(e, index));
}

function mouseIsDown(e, index){
  isDown = true;
  startY = e.pageY - container[index].offsetTop;
  startX = e.pageX - container[index].offsetLeft;
  scrollLeft = container[index].scrollLeft;
  scrollTop = container[index].scrollTop; 
}
function mouseUp(e){
  isDown = false;
}
function mouseLeave(e){
  isDown = false;
}
function mouseMove(e, index){
  if(isDown){
    e.preventDefault();
    //Move vertically
    const y = e.pageY - container[index].offsetTop;
    const walkY = y - startY;
    container[index].scrollTop = scrollTop - walkY;

    //Move Horizontally
    const x = e.pageX - container[index].offsetLeft;
    const walkX = x - startX;
    container[index].scrollLeft = scrollLeft - walkX;

  }
}