import { Upload, FileText, Settings, Download } from "lucide-react";

const steps = [
  {
    icon: Upload,
    title: "Upload CSV",
    description: "Upload your workout plan CSV file",
    gradient: "from-cyan-400 to-cyan-600",
  },
  {
    icon: FileText,
    title: "Preview Script",
    description: "Review the generated Vietnamese voice script",
    gradient: "from-blue-400 to-blue-600",
  },
  {
    icon: Settings,
    title: "Configure Audio",
    description: "Set beep cues, music, and volume levels",
    gradient: "from-violet-400 to-violet-600",
  },
  {
    icon: Download,
    title: "Download MP3",
    description: "Get your ready-to-play workout audio file",
    gradient: "from-cyan-400 to-blue-600",
  },
];

export default function WorkflowSteps() {
  return (
    <section className="relative py-24 px-4" id="workflow">
      <div className="max-w-5xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-5xl font-bold mb-4">
            How it works
          </h2>
          <p className="text-white/50 text-lg max-w-xl mx-auto">
            Four simple steps from your workout plan to a complete audio
            session.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 relative">
          {/* Connecting line */}
          <div className="hidden md:block absolute top-12 left-[12.5%] right-[12.5%] h-[2px] bg-gradient-to-r from-cyan-500/40 via-blue-500/40 to-violet-500/40" />

          {steps.map((step, index) => {
            const Icon = step.icon;
            return (
              <div key={step.title} className="relative flex flex-col items-center text-center group">
                <div
                  className={`w-24 h-24 rounded-2xl bg-gradient-to-br ${step.gradient} p-5 mb-6 shadow-xl shadow-${step.gradient.split(" ")[1]}/10 group-hover:scale-110 transition-transform duration-300 relative z-10`}
                >
                  <Icon className="w-full h-full text-white" />
                </div>
                <div className="glass-card rounded-2xl p-5 w-full">
                  <span className="text-2xl font-bold gradient-text block mb-1">
                    0{index + 1}
                  </span>
                  <h3 className="font-semibold mb-1">{step.title}</h3>
                  <p className="text-white/40 text-sm">{step.description}</p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}