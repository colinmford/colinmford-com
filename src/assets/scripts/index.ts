// import { Unit, convertUnits, splitUnitValue } from '@karibash/pixel-units';

let message: string = 'Hello World!';
// const gridWidth: Unit<'rem'> = '0.6rem';
// const gridHeight: Unit<'rem'> = '1.2rem';
const gridWidth: number = 9;
const gridHeight: number = 18;
console.log(message);

interface WindowSize {
  width: number
  height: number
}

function portraitResizer() {
  let size: WindowSize = {width: window.innerWidth, height: window.innerHeight}
  let columns: number = Math.floor(size.width/gridWidth);
  let rows: number = Math.floor(size.height/gridHeight);
  console.log("columns:", columns, "rows:", rows);
}

window.addEventListener("resize", () => {
  portraitResizer();
});

portraitResizer();

// for (let i: number = 0; i < 240; i++) {
//   let media: MediaQueryList = window.matchMedia("(max-width: 599px)")

// }

// @for $i from 40 through 240 {
//   @media (min-width: #{$i * $grid_size}) {
//     :root {
//     --columns: #{$i};
//     --media-query: '#{$i}';
//     }
//   }
// }
