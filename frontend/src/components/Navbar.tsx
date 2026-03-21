import { NavLink } from "./NavLink";
import { Menu, X, Moon, Sun } from "lucide-react";
import { useState, useEffect } from "react";
import { Button } from "./ui/button";
import { useLocation } from "react-router-dom";

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [isDark, setIsDark] = useState(true);
  const location = useLocation();

  // Check if we're on projects or blogs page
  const isOnProjectsOrBlogs = location.pathname === "/projects" || location.pathname === "/blogs";

  // Initialize theme from localStorage or system preference
  useEffect(() => {
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme) {
      setIsDark(savedTheme === "dark");
    } else {
      // Check if system prefers dark mode
      const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
      setIsDark(prefersDark);
    }
  }, []);

  // Apply theme to document
  useEffect(() => {
    const html = document.documentElement;
    if (isDark) {
      html.classList.add("dark");
    } else {
      html.classList.remove("dark");
    }
    localStorage.setItem("theme", isDark ? "dark" : "light");
  }, [isDark]);

  const toggleTheme = () => {
    setIsDark(!isDark);
  };

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-background/80 backdrop-blur-md border-b border-border">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <NavLink to="/" className="text-xl font-bold text-foreground hover:text-primary transition-colors shrink-0">
            Portfolio
          </NavLink>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8 flex-1 justify-end">
            <NavLink
              to="/"
              className="text-foreground hover:text-primary transition-colors"
              activeClassName="text-primary font-medium"
            >
              Home
            </NavLink>
            <NavLink
              to="/projects"
              className="text-foreground hover:text-primary transition-colors"
              activeClassName="text-primary font-medium"
            >
              Projects
            </NavLink>
            <NavLink
              to="/blogs"
              className="text-foreground hover:text-primary transition-colors"
              activeClassName="text-primary font-medium"
            >
              Blogs
            </NavLink>
            
            <Button 
              asChild 
              size="sm"
              disabled={isOnProjectsOrBlogs}
              className={isOnProjectsOrBlogs ? "opacity-50 cursor-not-allowed" : ""}
            >
              <a href={isOnProjectsOrBlogs ? "#" : "#contact"} onClick={(e) => isOnProjectsOrBlogs && e.preventDefault()}>
                Contact
              </a>
            </Button>

            {/* Theme Toggle Button - always on far right */}
            <button
              onClick={toggleTheme}
              className="p-2 rounded-lg hover:bg-muted transition-colors ml-16"
              aria-label="Toggle theme"
            >
              {isDark ? (
                <Sun size={20} className="text-foreground hover:text-primary transition-colors" />
              ) : (
                <Moon size={20} className="text-foreground hover:text-primary transition-colors" />
              )}
            </button>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center space-x-2">
            <button
              onClick={toggleTheme}
              className="p-2 rounded-lg hover:bg-muted transition-colors"
              aria-label="Toggle theme"
            >
              {isDark ? (
                <Sun size={20} className="text-foreground" />
              ) : (
                <Moon size={20} className="text-foreground" />
              )}
            </button>
            <button
              className="text-foreground"
              onClick={() => setIsOpen(!isOpen)}
            >
              {isOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isOpen && (
          <div className="md:hidden py-4 space-y-4">
            <NavLink
              to="/"
              className="block text-foreground hover:text-primary transition-colors"
              activeClassName="text-primary font-medium"
              onClick={() => setIsOpen(false)}
            >
              Home
            </NavLink>
            <NavLink
              to="/projects"
              className="block text-foreground hover:text-primary transition-colors"
              activeClassName="text-primary font-medium"
              onClick={() => setIsOpen(false)}
            >
              Projects
            </NavLink>
            <NavLink
              to="/blogs"
              className="block text-foreground hover:text-primary transition-colors"
              activeClassName="text-primary font-medium"
              onClick={() => setIsOpen(false)}
            >
              Blogs
            </NavLink>
            <Button 
              asChild 
              size="sm" 
              className={`w-full ${isOnProjectsOrBlogs ? "opacity-50 cursor-not-allowed" : ""}`}
              disabled={isOnProjectsOrBlogs}
            >
              <a 
                href={isOnProjectsOrBlogs ? "#" : "#contact"} 
                onClick={(e) => {
                  if (isOnProjectsOrBlogs) {
                    e.preventDefault();
                  } else {
                    setIsOpen(false);
                  }
                }}
              >
                Contact
              </a>
            </Button>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
