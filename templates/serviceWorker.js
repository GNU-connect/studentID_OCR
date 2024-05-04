// 구독 요청 함수
function subscribe() {
  if ("serviceWorker" in navigator) {
    navigator.serviceWorker
      .register("serviceWorker.js")
      .then(function (registration) {
        registration.pushManager
          .subscribe()
          .then(function (subscription) {
            console.log("Endpoint:", subscription.endpoint);
            // 구독 정보 백엔드 서버에 전송
            sendSubscriptionToServer(subscription);
            updateSubscriptionUI(true);
          })
          .catch(function (error) {
            console.error("Failed to subscribe:", error);
          });
      })
      .catch(function (error) {
        console.error("Failed to register service worker:", error);
      });
  } else {
    console.error("Push API is not supported");
  }
}
