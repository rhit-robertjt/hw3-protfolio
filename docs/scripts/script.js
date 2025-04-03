// Existing items that should be in the list
const existingList = ["milk", "eggs", "bread", "sugar"]

let checkForDuplicates = function (newItem, listSelector) {
  let duplicate = false;
  let listItems = document.querySelectorAll(listSelector);
  listItems.forEach(x => {
    if(newItem == x.textContent) {
      duplicate = true;
      return duplicate;
    }
  });
  return duplicate;
}

// TODO 1 - Complete this function to add an item to the existing list on the page
function addItemToList(itemString) {
  
  // check for duplicates
  if (checkForDuplicates(itemString, "#list1 li")
      || checkForDuplicates(itemString, "#list2 li")) {
    console.log("Skip duplicates.")
    return
  }

  // existingList.push(itemString);
  let list1 = document.querySelector("#list1");
  let list2 = document.querySelector("#list2");
  
  let li = document.createElement("li");
  li.textContent = itemString;
  list1.append(li);

  li.addEventListener("mouseover", function() {
    this.style.backgroundColor = "red";
    this.style.color = "white";
  });
  li.addEventListener("mouseout", function() {
    this.style.backgroundColor = "";
    this.style.color = "";
  });
  li.addEventListener("click", function() {
    console.log("Clicked on li " + itemString);
    if (list2.contains(this)) {
      // this.style.textDecoration = "";
      list1.appendChild(this);
    } else {
      // this.style.textDecoration = "line-through";
      list2.appendChild(this);
    }
  });
}

// TODO 2 - Complete this function to add all items from the existingList to the page
function addExistingList() {
    existingList.forEach(item => addItemToList(item));
}

// TODO 3 - Make it so that you don't have to run the command from the console, but
// instead it will run automatically.
function setupListener() {
    document.querySelector("#button1").addEventListener("click", () => {
        let textString = document.querySelector("#text1").value;
        if (textString.length > 0)
            addItemToList(textString);
    });
}

// document.addEventListener("DOMContentLoaded", setupListener);
// document.addEventListener("DOMContentLoaded", addExistingList);
window.addEventListener("load", (event) => {
    console.log("Event Occurred: " + event);
    console.log("Page fully loaded.");
    setupListener();
    addExistingList();
})
