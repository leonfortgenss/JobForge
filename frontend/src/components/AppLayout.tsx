
// import Nav from "../_components/Nav";
// import Footer from "../_components/Footer";


export default function AppLayout({
  children,
}: {
  children: React.ReactNode
}) {

  return (
    <>
        <nav className="flex flex-col min-h-screen w-full">
            {/* <Nav /> */}
            <ul>
                <li>Home</li>
                <li>Personal Letter</li>
                <li>Historical Data</li>
            </ul>
        </nav>
        <main>
            {children}
        </main>
        <footer className="mt-auto">
            {/* <Footer /> */}
            <ul>
                <li>Home</li>
                <li>Personal Letter</li>
                <li>Historical Data</li>
                <li>Contact</li>
            </ul>
        </footer>
    </>
  );
}