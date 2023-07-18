function deleteTrip(tripId) {
  fetch("/delete-trip", {
    method: "POST",
    body: JSON.stringify({ tripId: tripId }),
  }).then((_res) => {
    window.location.href = "/mytrips";
  });
}
