import { Github, Linkedin, Mail, Twitter } from "lucide-react";

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="border-t border-border bg-muted/30 py-12 px-4 sm:px-6 lg:px-8">
      <div className="container mx-auto">
        <div className="max-w-6xl mx-auto">
          <div className="flex flex-col md:flex-row justify-between items-center gap-6">
            <div className="text-center md:text-left">
              <h3 className="text-xl font-bold text-foreground mb-2">Portfolio</h3>
              <p className="text-muted-foreground">
                Building the future, one line at a time.
              </p>
            </div>

            <div className="flex gap-4">
              <a
                href="https://github.com/AdityaZala3919"
                target="_blank"
                rel="noopener noreferrer"
                className="p-3 rounded-full border border-border hover:border-primary hover:bg-primary/10 transition-all"
              >
                <Github className="h-5 w-5" />
              </a>
              <a
                href="https://www.linkedin.com/in/adityasinh-zala-1bbb42258/"
                target="_blank"
                rel="noopener noreferrer"
                className="p-3 rounded-full border border-border hover:border-primary hover:bg-primary/10 transition-all"
              >
                <Linkedin className="h-5 w-5" />
              </a>
              <a
                href="https://twitter.com"
                target="_blank"
                rel="noopener noreferrer"
                className="p-3 rounded-full border border-border hover:border-primary hover:bg-primary/10 transition-all"
              >
                <Twitter className="h-5 w-5" />
              </a>
              <a
                href="mailto:adityazala404@gmail.com"
                className="p-3 rounded-full border border-border hover:border-primary hover:bg-primary/10 transition-all"
              >
                <Mail className="h-5 w-5" />
              </a>
            </div>
          </div>

          <div className="mt-8 pt-8 border-t border-border text-center text-muted-foreground">
            <p>© {currentYear} Aditya Zala. All rights reserved.</p>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
