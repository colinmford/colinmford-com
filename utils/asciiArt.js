const imageToAscii = require("image-to-ascii");

// Passing options
imageToAscii("/Users/colinmford/Downloads/IMG_0499.jpg", {
    colored: false,
    preserve_aspect_ratio: true,
    size: {
      height: "100%"
    },
    pixels: " .:*◆░▒▓"
}, (err, converted) => {
    console.log(err || converted);
});
