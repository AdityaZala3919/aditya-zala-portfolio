import { Brain, Database, Rocket } from "lucide-react";
import { Card, CardContent } from "./ui/card";

const About = () => {
  const skills = [
    {
      icon: Brain,
      title: "AI & Machine Learning",
      description:
        "Building intelligent systems using deep learning, NLP, and transformers, including projects like image captioning and LLM-based applications.",
    },
    {
      icon: Database,
      title: "Backend & Systems",
      description:
        "Developing scalable backend systems with Python, APIs, and vector databases for real-world AI applications like RAG systems.",
    },
    {
      icon: Rocket,
      title: "Innovation & Projects",
      description:
        "Continuously experimenting with cutting-edge technologies, from building models from scratch to deploying end-to-end AI solutions.",
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
              I'm an AI/ML Engineer passionate about building intelligent, real-world applications.
              I specialize in deep learning, NLP, and backend systems, and enjoy transforming complex ideas into scalable, impactful solutions.
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