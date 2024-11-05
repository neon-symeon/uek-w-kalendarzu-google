document.addEventListener("DOMContentLoaded", function () {
  // Zaznaczanie/odznaczanie wszystkich checkboxów
  const checkAllBox = document.getElementById("check-all");
  const checkboxes = document.querySelectorAll(".select-item");

  checkAllBox.addEventListener("change", function () {
    const isChecked = this.checked;
    checkboxes.forEach(function (checkbox) {
      checkbox.checked = isChecked;
    });
  });
});

// Funkcja do zebrania wybranych zajęć i przesłania ich do widoku Django
function submitSelectedEvents() {
  const selectedEvents = [];

  // Wydkrukuj kliknięcie przycisku
  console.log(
    "*** Przycisk 'Dodaj wybrane zajęcia do Google Calendar' został kliknięty."
  );

  // Przechodzimy przez wszystkie zaznaczone checkboxy i zbieramy pełne dane o wydarzeniach
  document
    .querySelectorAll(".select-item:checked")
    .forEach(function (checkbox) {
      const eventData = JSON.parse(checkbox.getAttribute("data-event"));

      // Konwersja dat na ISO
      eventData.start = new Date(eventData.start).toISOString();
      eventData.end = new Date(eventData.end).toISOString();

      selectedEvents.push(eventData);
    });

  // Przypisanie wybranych zajęć jako JSON do ukrytego pola formularza
  document.getElementById("selectedEventsInput").value =
    JSON.stringify(selectedEvents);

  // Wyświetlenie informacji o wybranych zajęć
  console.log("Wybrane zajęcia: ", selectedEvents);

  // Przesłanie formularza
  document.getElementById("selectedEventsForm").submit();
}
