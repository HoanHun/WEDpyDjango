// Custom JS cho Fashion Shop

document.addEventListener('DOMContentLoaded', function () {
    // Tự động ẩn các thông báo (alert) sau 4 giây
    var alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            var bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 4000);
    });
});
