import {
  Upload,
  Languages,
  Timeline,
  Bell,
  Music,
  Download,
} from "lucide-react";

const features = [
  {
    icon: Upload,
    title: "CSV Workout Import",
    description:
      "Upload your workout plan as a CSV file. Simple format, instant processing.",
    gradient: "from-cyan-400 to-cyan-600",
  },
  {
    icon: Languages,
    title: "Vietnamese Voice Guidance",
    description:
      "Professional Vietnamese TTS voice coaching for each exercise and rest period.",
    gradient: "from-blue-400 to-blue-600",
  },
  {
    icon: Timeline,
    title: "Work/Rest Timeline",
    description:
      "Intelligent timeline that alternates between exercise instructions and rest periods.",
    gradient: "from-violet-400 to-violet-600",
  },
  {
    icon: Bell,
    title: "Beep Cues",
    description:
      "Audible beep alerts before transitions so you never miss a switch.",
    gradient: "from-cyan-400 to-violet-600",
  },
  {
    icon: Music,
    title: "Background Music",
    description:
      "Optional background music with smart volume ducking during voice cues.",
    gradient: "from-blue-400 to-violet-600",
  },
  {
    icon: Download,
    title: "MP3 Export",
    description:
      "Download a production-ready MP3 file. Play it on any device or player.",
    gradient: "from-cyan-400 to-blue-600",
  },
];

export default function FeatureGrid() {
  return (
    <section className="relative py-24 px-4" id="features">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-5xl font-bold mb-4">
            Everything you need
          </h2>
          <p className="text-white/50 text-lg max-w-xl mx-auto">
            From CSV import to MP3 download — a complete workout audio
            pipeline.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature) => {
            const Icon = feature.icon;
            return (
              <div
                key={feature.title}
                className="glass-card-hover rounded-2xl p-6 group"
              >
                <div
                  className={`w-12 h-12 rounded-xl bg-gradient-to-br ${feature.gradient} p-2.5 mb-4 shadow-lg`}
                >
                  <Icon className="w-full h-full text-white" />
                </div>
                <h3 className="text-lg font-semibold mb-2">{feature.title}</h3>
                <p className="text-white/50 text-sm leading-relaxed">
                  {feature.description}
                </p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}