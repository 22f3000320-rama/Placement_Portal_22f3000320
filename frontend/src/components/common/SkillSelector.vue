<template>
    <div v-if="editable">

        <input type="text" class="form-control mb-2" v-model="search" :placeholder="placeholder">

        <div class="border rounded p-2 mb-3" style="max-height:220px; overflow-y:auto;">
            <div v-for="skill in filteredSkills" :key="skill" class="form-check">
                <input class="form-check-input" type="checkbox" :id="skill" :value="skill"
                    :checked="selectedSkills.includes(skill)" @change="toggleSkill(skill)">

                <label class="form-check-label" :for="skill">
                    {{ skill }}
                </label>
            </div>

            <div v-if="filteredSkills.length === 0" class="text-muted">
                No matching skills found.
            </div>
        </div>

        <div v-if="selectedSkills.length">
            <span v-for="skill in selectedSkills" :key="skill" class="badge bg-primary me-2 mb-2">
                {{ skill }}

                <button type="button" class="btn-close btn-close-white ms-2" style="font-size:0.5rem"
                    @click="toggleSkill(skill)"></button>
            </span>
        </div>
    </div>

    <div v-else>
        <span v-for="skill in selectedSkills" :key="skill" class="badge bg-primary me-2 mb-2">
            {{ skill }}
        </span>
        <p v-if="selectedSkills.length === 0" class="text-muted">
            No skills added.
        </p>

    </div>
</template>

<script>
    export default {
        name: "SkillSelector",

        props: {
            modelValue: {
                type: Array,
                default: () => []
            },
            editable: {
                type: Boolean,
                default: false
            },
            options: {
                type: Array,
                default: () => []
            },
            placeholder: {
                type: String,
                default: "Search skills..."
            }
        },

        emits: ["update:modelValue"],

        data() {
            return {
                search: "",
                allSkills: [
                    "C",
                    "C++",
                    "Java",
                    "Python",
                    "JavaScript",
                    "TypeScript",
                    "SQL",
                    "HTML",
                    "CSS",
                    "Bootstrap",
                    "Vue.js",
                    "React",
                    "Angular",
                    "Node.js",
                    "Express.js",
                    "Flask",
                    "Django",
                    "Spring Boot",
                    "MongoDB",
                    "MySQL",
                    "PostgreSQL",
                    "Git",
                    "GitHub",
                    "Docker",
                    "AWS",
                    "Linux",
                    "Machine Learning",
                    "Data Science",
                    "TensorFlow",
                    "PyTorch"
                ]
            };
        },

        computed: {
            selectedSkills() {
                return this.modelValue;
            },
            filteredSkills() {
                return this.allSkills.filter(skill =>
                    skill.toLowerCase().includes(
                        this.search.toLowerCase()
                    )
                );
            }
        },

        methods: {
            toggleSkill(skill) {
                let updated = [...this.selectedSkills];

                if (updated.includes(skill)) {
                    updated = updated.filter(s => s !== skill);
                } else {
                    updated.push(skill);
                }

                this.$emit("update:modelValue", updated);
            }
        }
    };
</script>