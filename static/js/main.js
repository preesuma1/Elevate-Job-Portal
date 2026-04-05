// Auto-dismiss alerts
document.addEventListener('DOMContentLoaded', function () {
  setTimeout(() => {
    document.querySelectorAll('.alert.show').forEach(el => {
      const alert = bootstrap.Alert.getOrCreateInstance(el);
      alert.close();
    });
  }, 5000);

  // Active nav link highlight
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-link').forEach(link => {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
    }
  });
});