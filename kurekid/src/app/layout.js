export default function DashboardLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <h1>Default Layout</h1>
        {/* Layout UI */}
        {/* Place children where you want to render a page or nested layout */}
        <main>{children}</main>
      </body>
    </html>
  )
}