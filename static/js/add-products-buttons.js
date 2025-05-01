console.log("JavaScript is running");
// const data = {
//   men: {
//     "T-shirts": {
//       "Half Sleeve T-shirts": {
//         "Polo T-shirts": null,
//         "Round-Neck T-shirts": null,
//         "V-Neck T-shirts": null,
//         "Henley T-shirts": null,
//         "Graphic T-shirts": null
//       },
//       "Full Sleeve T-shirts": {
//         "Full Sleeve Polo T-shirts": null,
//         "Full Sleeve Round Neck T-shirts": null,
//         "Thermal T-shirts": null
//       }
//     },
//     "Shirts": {
//       "Formal Shirts": null,
//       "Casual Shirts": null,
//       "Denim Shirts": null,
//       "Linen Shirts": null
//     },
//     "Jeans": {
//       "Slim Fit Jeans": null,
//       "Regular Fit Jeans": null,
//       "Skinny Fit Jeans": null,
//       "Ripped Jeans": null
//     },
//     "Lowers": {
//       "Track Pants": null,
//       "Joggers": null,
//       "Cotton Lowers": null
//     },
//     "Jackets": {
//       "Bomber Jackets": null,
//       "Denim Jackets": null,
//       "Leather Jackets": null,
//       "Puffer Jackets": null
//     },
//     "Hoodies": {
//       "Zipper Hoodies": null,
//       "Pullover Hoodies": null
//     },
//     "Suits": {
//       "Formal Suits": null,
//       "Tuxedos": null
//     },
//     "Sweater": {
//       "V-Neck Sweater": null,
//       "Crew Neck Sweater": null
//     },
//     "Shorts": {
//       "Denim Shorts": null,
//       "Cotton Shorts": null
//     },
//     "Tank Top": {
//       "Gym Tank Tops": null,
//       "Casual Tank Tops": null
//     }
//   },

//   women: {
//     "Kurtis": {
//       "Straight Kurtis": null,
//       "Anarkali Kurtis": null,
//       "A-line Kurtis": null
//     },
//     "Suits": {
//       "Salwar Suits": null,
//       "Palazzo Suits": null,
//       "Churidar Suits": null
//     },
//     "Tops": {
//       "Crop Tops": null,
//       "Tunic Tops": null,
//       "Peplum Tops": null
//     },
//     "Jeans": {
//       "High Waist Jeans": null,
//       "Skinny Jeans": null,
//       "Bootcut Jeans": null
//     },
//     "Leggings": {
//       "Printed Leggings": null,
//       "Solid Leggings": null
//     },
//     "Sarees": {
//       "Silk Sarees": null,
//       "Cotton Sarees": null,
//       "Designer Sarees": null
//     },
//     "Dresses": {
//       "Maxi Dresses": null,
//       "Bodycon Dresses": null,
//       "A-line Dresses": null
//     },
//     "Skirts": {
//       "Mini Skirts": null,
//       "Long Skirts": null
//     },
//     "Sweaters": {
//       "Cardigans": null,
//       "Pullover Sweaters": null
//     },
//     "Jackets": {
//       "Blazers": null,
//       "Denim Jackets": null
//     }
//   }
// };

// // const data = {
// //   "Men": {
// //     "T-Shirts": {
// //       "Half Sleeve T-Shirts": ["Polo T-Shirts", "Round Neck T-Shirts", "V-Neck T-Shirts", "Henley T-Shirts", "Sweatshirts"],
// //       "Full Sleeve T-Shirts": ["Striped T-Shirts", "Plain T-Shirts", "Graphic T-Shirts"]
// //     },
// //     "Shirts": ["Formal Shirts", "Casual Shirts", "Denim Shirts", "Printed Shirts"],
// //     "Jeans": ["Slim Fit Jeans", "Regular Fit Jeans", "Tapered Jeans"],
// //     "Lowers": ["Track Pants", "Joggers", "Pyjamas"],
// //     "Jackets": ["Bomber Jackets", "Denim Jackets", "Leather Jackets"],
// //     "Hoodies": ["Zip-up Hoodies", "Pullover Hoodies"],
// //     "Suits": ["Business Suits", "Wedding Suits"],
// //     "Sweater": ["Crew Neck Sweater", "V-Neck Sweater"],
// //     "Shorts": ["Casual Shorts", "Sports Shorts"],
// //     "Tank Top": ["Gym Tank Tops", "Casual Tank Tops"]
// //   },
// //   "Women": {
// //     "Kurtis": ["Anarkali Kurtis", "Straight Kurtis", "A-line Kurtis"],
// //     "Suits": ["Salwar Suits", "Anarkali Suits", "Straight Suits", "A-line Suits", "Churidar Suits"],
// //     "Tops": ["Crop Tops", "Blouse Tops", "Off-Shoulder Tops"],
// //     "Dresses": ["Maxi Dresses", "Bodycon Dresses", "A-Line Dresses"],
// //     "Jeans": ["Skinny Jeans", "Boyfriend Jeans", "High-waist Jeans"],
// //     "Skirts": ["Mini Skirts", "Pencil Skirts"],
// //     "Jackets": ["Denim Jackets", "Blazers"],
// //     "Sweaters": ["Pullover Sweaters", "Cardigans"]
// //   }
// // };


// function createCategoryItem(text, onclickFn, parentGridId) {
//   const div = document.createElement('div');
//   div.className = 'category-item';
//   div.onclick = function() {
//     setActive(this, parentGridId);
//     if (onclickFn) onclickFn();
//   };

//   const icon = document.createElement('i');
//   icon.className = 'fas fa-tag'; // default icon

//   const span = document.createElement('span');
//   span.innerText = text;

//   div.appendChild(icon);
//   div.appendChild(span);
//   return div;
// }

// function setActive(element, gridId) {
//   const parent = document.getElementById(gridId);
//   const items = parent.querySelectorAll('.category-item');
//   items.forEach(item => item.classList.remove('active'));
//   element.classList.add('active');
// }

// function showCategory(gender) {
//   const subcategoryDiv = document.getElementById('subcategory');
//   const subsubcategoryDiv = document.getElementById('subsubcategory');
//   const finalcategoryDiv = document.getElementById('finalcategory');

//   subcategoryDiv.innerHTML = '';
//   subsubcategoryDiv.innerHTML = '';
//   finalcategoryDiv.innerHTML = '';

//   for (let item in data[gender]) {
//     const div = createCategoryItem(item, () => showSubCategory(gender, item), 'subcategory');
//     subcategoryDiv.appendChild(div);
//   }
// }

// function showSubCategory(gender, item) {
//   const subsubcategoryDiv = document.getElementById('subsubcategory');
//   const finalcategoryDiv = document.getElementById('finalcategory');

//   subsubcategoryDiv.innerHTML = '';
//   finalcategoryDiv.innerHTML = '';

//   const subitems = data[gender][item];
//   if (subitems) {
//     for (let subitem in subitems) {
//       const div = createCategoryItem(subitem, () => showFinalCategory(gender, item, subitem), 'subsubcategory');
//       subsubcategoryDiv.appendChild(div);
//     }
//   }
// }

// function showFinalCategory(gender, item, subitem) {
//   const finalcategoryDiv = document.getElementById('finalcategory');
//   finalcategoryDiv.innerHTML = '';

//   const finalitems = data[gender][item][subitem];
//   if (finalitems) {
//     for (let final in finalitems) {
//       const div = createCategoryItem(final, null, 'finalcategory');
//       finalcategoryDiv.appendChild(div);
//     }
//   }
// }


const data = {
  "Men": {
    "T-Shirts": {
      "Half Sleeve T-Shirts": ["Polo T-Shirts", "Round Neck T-Shirts", "V-Neck T-Shirts", "Henley T-Shirts", "Sweatshirts"],
      "Full Sleeve T-Shirts": ["Striped T-Shirts", "Plain T-Shirts", "Graphic T-Shirts"]
    },
    "Shirts": ["Formal Shirts", "Casual Shirts", "Denim Shirts", "Printed Shirts"],
    "Jeans": ["Slim Fit Jeans", "Regular Fit Jeans", "Tapered Jeans"],
    "Lowers": ["Track Pants", "Joggers", "Pyjamas"],
    "Jackets": ["Bomber Jackets", "Denim Jackets", "Leather Jackets"],
    "Hoodies": ["Zip-up Hoodies", "Pullover Hoodies"],
    "Suits": ["Business Suits", "Wedding Suits"],
    "Sweater": ["Crew Neck Sweater", "V-Neck Sweater"],
    "Shorts": ["Casual Shorts", "Sports Shorts"],
    "Tank Top": ["Gym Tank Tops", "Casual Tank Tops"]
  },
  "Women": {
    "Kurtis": ["Anarkali Kurtis", "Straight Kurtis", "A-line Kurtis"],
    "Suits": ["Salwar Suits", "Anarkali Suits", "Straight Suits", "A-line Suits", "Churidar Suits"],
    "Tops": ["Crop Tops", "Blouse Tops", "Off-Shoulder Tops"],
    "Dresses": ["Maxi Dresses", "Bodycon Dresses", "A-Line Dresses"],
    "Jeans": ["Skinny Jeans", "Boyfriend Jeans", "High-waist Jeans"],
    "Skirts": ["Mini Skirts", "Pencil Skirts"],
    "Jackets": ["Denim Jackets", "Blazers"],
    "Sweaters": ["Pullover Sweaters", "Cardigans"]
  }
};


// Image file mapping (real filenames)
const images = {};
Object.keys(data).forEach(gender => {
  Object.keys(data[gender]).forEach(category => {
    const sub = data[gender][category];
    if (typeof sub === 'object' && !Array.isArray(sub)) {
      // sub is an object (example: T-Shirts have Half Sleeve, Full Sleeve)
      Object.keys(sub).forEach(subCategory => {
        const finalSub = sub[subCategory];
        if (Array.isArray(finalSub)) {
          finalSub.forEach(final => {
          images[final] = Array.from({ length: 5 }, (_, i) => `/static/img/models/${gender.toLowerCase()}/${category.toLowerCase().replace(/\s/g,'-')}/${subCategory.toLowerCase().replace(/\s/g,'-')}/${final.toLowerCase().replace(/\s/g,'-')}/${final.toLowerCase().replace(/\s/g,'-')}-${i+1}.png`);
          });
        }
      });
    } else if (Array.isArray(sub)){
      sub.forEach(final => {
        images[final] = Array.from({ length: 5 }, (_, i) => `/static/img/models/${gender.toLowerCase()}/${category.toLowerCase().replace(/\s/g,'-')}/${final.toLowerCase().replace(/\s/g,'-')}/${final.toLowerCase().replace(/\s/g,'-')}-${i+1}.png`);
      });
    }
  });
});

const categoryGrid = document.querySelector('.category-grid');
const subCategoryGrid = document.querySelector('.sub-category-grid');
const finalCategoryGrid = document.querySelector('.final-category-grid');
const finalSubCategoryGrid = document.querySelector('.final-sub-category-grid');
const imagesSection = document.querySelector('.images-section');
const heading = document.getElementById('image-section-heading');
const detailBox = document.getElementById("result-image-box");
const spinner = document.querySelector('.spinner');

let selectedImagePath = "";

function clearGrid(grid) {
  grid.innerHTML = '';
}


// Attach Click Listener to whole category grid
categoryGrid.addEventListener('click', function (e) {
  const target = e.target.closest('[data-gender]');
  if (!target) return;

  const gender = target.dataset.gender;
  console.log("Selected gender:", gender);
  showSubCategories(gender);

  // Optional: Active class handling
  Array.from(categoryGrid.children).forEach(item => item.classList.remove('active'));
  target.classList.add('active');
});

function createCategoryItem(name, icon = 'fas fa-tshirt') {
  console.log("1")
  const div = document.createElement('div');
  div.className = 'category-item';
  div.innerHTML = `<i class="${icon}"></i><span>${name}</span>`;
  div.addEventListener('click', () => {
    // Active class handling
    const siblings = div.parentElement.querySelectorAll('.category-item');
    siblings.forEach(sib => sib.classList.remove('active'));
    div.classList.add('active');
  });
  return div;
}

function showSubCategories(gender) {
  console.log("1")
  clearGrid(subCategoryGrid);
  clearGrid(finalCategoryGrid);
  clearGrid(finalSubCategoryGrid);
  clearGrid(imagesSection);
  heading.style.display = 'none';
  detailBox.style.display = "none";

  const categories = Object.keys(data[gender]);
  console.log("2")
  categories.forEach(cat => {
    const item = createCategoryItem(cat);
    item.addEventListener('click', () => showFinalCategories(gender, cat));
    subCategoryGrid.appendChild(item);
  });
}

function showFinalCategories(gender, category) {
  clearGrid(finalCategoryGrid);
  clearGrid(finalSubCategoryGrid);
  clearGrid(imagesSection);
  heading.style.display = 'none';
  detailBox.style.display = "none";

  const sub = data[gender][category];
  console.log("5")
  console.log(sub)
  if (Array.isArray(sub)) {
    console.log("6")
    sub.forEach(subCat => {
      const item = createCategoryItem(subCat);
      item.addEventListener('click', () => showImages(subCat));
      finalCategoryGrid.appendChild(item);
    });
  } else if (typeof sub === 'object') {
    const subCategories = Object.keys(sub);
    subCategories.forEach(subCat => {
      console.log("7")
      const item = createCategoryItem(subCat);
      item.addEventListener('click', () => showFinalSubCategories(gender, category, subCat));
      finalCategoryGrid.appendChild(item);
    });
  }
}

function showFinalSubCategories(gender, category, subCat) {
  clearGrid(finalSubCategoryGrid);
  clearGrid(imagesSection);
  heading.style.display = 'none';
  detailBox.style.display = "none";

  const sub = data[gender][category][subCat];
  if (Array.isArray(sub)) {
    sub.forEach(final => {
      const item = createCategoryItem(final);
      item.addEventListener('click', () => showImages(final));
      finalSubCategoryGrid.appendChild(item);
    });
  }
}

function showImages(final) {
  clearGrid(imagesSection);
  
  // Show Heading
  heading.style.display = 'block';
  heading.textContent = `Choose Models`;

  spinner.style.display = 'block';
  setTimeout(() => {
    spinner.style.display = 'none';
    images[final].forEach(src => {
      const img = document.createElement('img');
      img.src = src;
      img.alt = final;
      img.loading = "lazy";
      img.style.width = "200px";
      img.style.height = "250px";
      img.style.objectFit = "contain";
      img.style.margin = "10px";
      img.className = 'image-item'; // <-- add class

      img.addEventListener('click', function() {
        // Remove active from all images
        document.querySelectorAll('.images-section img').forEach(i => i.classList.remove('active'));
        // Add active to clicked image
        this.classList.add('active');

        detailBox.style.display = "block";
        detailBox.style.margin = "10px";

        selectedImagePath = this.src;
        console.log("Selected image path:", selectedImagePath);
      });
      imagesSection.appendChild(img);
    });
  }, 500);
}


async function uploadImages() {
  const modelImage = selectedImagePath;
  const garmentImage = document.getElementById("product-image").files[0]; 

  if (!modelImage || !garmentImage) {
    alert("Please select both images.");
    return;
  }   

  const formData = new FormData();

  formData.append("garment_image", garmentImage);

  const response2 = await fetch(modelImage);
  const blob2 = await response2.blob();
  formData.append("model_image", blob2, "model_image.jpg");

  try {
    const response = await fetch('/upload', {
      method: 'POST',
      body: formData
    });   

    const result = await response.json();

    if (result.output) {
      document.getElementById("result-heading").style.display="block";
      // document.getElementById('resultImage').src = result.output;
      document.getElementById('resultImage').src = result.upscaled_url;
      document.getElementById('resultImage').style.display = 'block';
    } else {
      document.getElementById('response').innerText = result.error || 'Error processing image.';
    }
  } catch (error) {
    console.error("Error:", error);
    document.getElementById('response').innerText = "Error occurred while processing.";
  }
}
