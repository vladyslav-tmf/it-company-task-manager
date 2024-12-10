document.addEventListener("DOMContentLoaded", function() {
     const languageSelect = document.querySelector(".language-select");
     if (languageSelect) {
       languageSelect.addEventListener("change", function() {
         document.getElementById("languageForm").submit();
       });
     }
   });
