import { Code2, Palette, Rocket } from "lucide-react";
import { Card, CardContent } from "./ui/card";

const About = () => {
  const skills = [
    {
      icon: Code2,
      title: "Development",
      description: "Building scalable applications with modern technologies and best practices.",
    },
    {
      icon: Palette,
      title: "Design",
      description: "Creating intuitive and beautiful user interfaces that delight users.",
    },
    {
      icon: Rocket,
      title: "Innovation",
      description: "Always learning and implementing cutting-edge solutions.",
    },
  ];

  return (
    <section className="py-20 px-4 sm:px-6 lg:px-8 bg-muted/30">
      <div className="container mx-auto">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-foreground mb-4">
              About Me
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              I'm a passionate developer with expertise in building modern web applications.
              I love turning complex problems into simple, beautiful, and intuitive solutions.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {skills.map((skill, index) => (
              <Card
                key={index}
                className="border-border hover:border-primary transition-all duration-300 hover:shadow-lg"
              >
                <CardContent className="pt-6">
                  <div className="mb-4 inline-flex p-3 rounded-lg bg-primary/10">
                    <skill.icon className="h-6 w-6 text-primary" />
                  </div>
                  <h3 className="text-xl font-semibold text-foreground mb-2">
                    {skill.title}
                  </h3>
                  <p className="text-muted-foreground">{skill.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default About;
