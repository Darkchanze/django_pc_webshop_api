export function isLoggedIn() {
  const token = localStorage.getItem('accessToken');
  if (!token) return false;

  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    const issuedAt = payload.iat;
    const now = Math.floor(Date.now() / 1000);
    const maxLifetime = 60 * 60; // 1 hour

    return now - issuedAt < maxLifetime;
  } catch {
    return false;
  }
}
export function logout() {
  localStorage.removeItem('accessToken');
  localStorage.removeItem('refreshToken');
}
