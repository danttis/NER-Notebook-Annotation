import json
import uuid

from IPython.display import HTML, display


class TextClassifier:
    """
    Class for classifying text documents in a Jupyter Notebook.

    Allows assigning labels to whole texts, navigating through a list
    of documents, and exporting results.
    """

    def __init__(
        self,
        texts: list,
        labels: list = None,
        custom_colors: dict = None,
        session_id: str = None
    ):
        """
        Initializes the classifier.

        Args:
            texts: List of strings to be classified.
            labels: List of classification labels.
            custom_colors: Map of labels to hexadecimal colors.
            session_id: Optional session identifier.
        """
        self.texts = texts
        self.current_index = 0
        self.classifications = {}

        if labels is None:
            labels = ["Positive", "Negative", "Neutral"]
        self.labels = labels

        if custom_colors is None:
            base_colors = ["#4caf50", "#f44336", "#2196f3", "#ff9800"]
            custom_colors = {
                labels[i]: base_colors[i % len(base_colors)]
                for i in range(len(labels))
            }
        self.custom_colors = custom_colors

        if session_id is None:
            session_id = str(uuid.uuid4())[:8]
        self.session_id = session_id

    def render(self, variable_name: str = None):
        """
        Renders the classification interface.

        Args:
            variable_name: Name of the Python variable for export.
        """
        font_url = (
            "https://fonts.googleapis.com/css2?family=Inter:"
            "wght@400;500;600;700;800&display=swap"
        )
        gh_btn_url = (
            "https://ghbtns.com/github-btn.html?user=danttis"
            "&repo=NER-Notebook-Annotation&type=watch&count=true"
            "&size=large&v=2"
        )

        main_html = """
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="{3}" rel="stylesheet">
        <style>
            :root {{
                --primary: #4F46E5;
                --bg-body: #F3F4F6;
                --bg-card: #FFFFFF;
                --text-main: #1F2937;
                --border-color: #E5E7EB;
            }}
            #cls_main_{0} {{
                font-family: 'Inter', -apple-system, sans-serif;
                background-color: var(--bg-body);
                padding: 20px;
                color: var(--text-main);
                border-radius: 20px;
            }}
            .main-layout-{0} {{
                display: grid;
                grid-template-columns: 1fr 300px;
                gap: 20px;
                max-width: 1200px;
                margin: 0 auto;
            }}
            .editor-section-{0} {{
                background: var(--bg-card);
                padding: 25px;
                border-radius: 16px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                border: 1px solid var(--border-color);
            }}
            .sidebar-section-{0} {{
                background: var(--bg-card);
                padding: 20px;
                border-radius: 16px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                border: 1px solid var(--border-color);
                height: fit-content;
            }}
            .nav-bar-{0} {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
                background: #F9FAFB;
                padding: 12px;
                border-radius: 10px;
            }}
            .text-display-{0} {{
                font-size: 1.15rem;
                line-height: 1.8;
                padding: 25px;
                border: 2px solid #F3F4F6;
                border-radius: 12px;
                min-height: 200px;
                margin-bottom: 20px;
                background: #fff;
                outline: none;
                user-select: text;
                white-space: pre-wrap;
                color: #000;
            }}
            .label-list-{0} {{
                display: flex;
                flex-direction: column;
                gap: 10px;
                margin-top: 15px;
            }}
            .label-item-{0} {{
                display: flex;
                align-items: center;
                padding: 12px;
                border-radius: 8px;
                font-size: 0.9rem;
                font-weight: 600;
                border: 2px solid transparent;
                cursor: pointer;
                transition: all 0.2s;
            }}
            .label-dot-{0} {{
                width: 12px;
                height: 12px;
                border-radius: 50%;
                margin-right: 12px;
            }}
            .btn-{0} {{
                padding: 10px 18px;
                border-radius: 8px;
                border: none;
                cursor: pointer;
                font-weight: 600;
                transition: 0.2s;
            }}
            .btn-nav-{0} {{
                background: white;
                border: 1px solid var(--border-color);
            }}
            .btn-nav-{0}:disabled {{ opacity: 0.3; }}
            .btn-action-{0} {{
                margin: 5px;
                color: white;
                font-size: 14px;
            }}
        </style>
        <div id="cls_main_{0}">
            <div class="main-layout-{0}">
                <div class="editor-section-{0}">
                    <div class="nav-bar-{0}">
                        <button id="btnPrev_{0}"
                                class="btn-{0} btn-nav-{0}">
                            ← Anterior
                        </button>
                        <span id="textCounter_{0}"
                              style="font-weight: 700; color: #000;">
                            Doc 1 / {1}
                        </span>
                        <button id="btnNext_{0}"
                                class="btn-{0} btn-nav-{0}">
                            Próximo →
                        </button>
                    </div>
                    <div id="textsContainer_{0}" class="text-display-{0}">
                    </div>
                    <div style="text-align:center; margin-top:20px;
                                border-top: 1px solid #eee; padding-top:20px;">
                        <button id="btnDownloadAll_{0}"
                                class="btn-{0} btn-action-{0}"
                                style="background:#2196f3;">
                            📥 Download JSON
                        </button>
                    </div>
                </div>
                <div class="sidebar-section-{0}">
                    <h3 style="margin:0; color: #000;">🏷️ Classificar</h3>
                    <p style="font-size: 0.8rem; color: #6B7280;">
                        Selecione a classe para o documento atual.
                    </p>
                    <div id="labelList_{0}" class="label-list-{0}">
                        {2}
                    </div>
                    <hr style="border:0; border-top:1px solid #eee;
                               margin:20px 0;">
                    <div style="margin-top: 20px;">
                         <iframe src="{4}" frameborder="0" scrolling="0"
                                 width="170" height="30" title="GitHub">
                         </iframe>
                    </div>
                </div>
            </div>
        </div>
        """.format(
            self.session_id,
            len(self.texts),
            "".join([
                (
                    '<div class="label-item-{0}" '
                    'onclick="setLabel(\'{1}\')" '
                    'style="border-color:{2}; color:{2};" '
                    'id="label_btn_{0}_{1}">'
                    '<span class="label-dot-{0}" '
                    'style="background:{2}"></span>'
                    '{1}</div>'
                ).format(
                    self.session_id, label, self.custom_colors[label]
                ) for label in self.labels
            ]),
            font_url,
            gh_btn_url
        )

        js_code = """
        <script>
        (function() {{
            const sessionId = '{0}';
            const texts = {1};
            const customColors = {2};
            let currentIndex = 0;
            let classifications = {{}};

            function getText(idx) {{
                const item = texts[idx];
                return Array.isArray(item) ? item[1] : String(item);
            }}

            function getId(idx) {{
                const item = texts[idx];
                return Array.isArray(item) ? String(item[0]) : String(idx);
            }}

            const container = document.getElementById(
                'textsContainer_' + sessionId
            );
            const counter = document.getElementById(
                'textCounter_' + sessionId
            );
            const btnPrev = document.getElementById('btnPrev_' + sessionId);
            const btnNext = document.getElementById('btnNext_' + sessionId);

            window.setLabel = function(label) {{
                classifications[currentIndex] = label;
                updateDisplay();
                // Auto-advance
                if (currentIndex < texts.length - 1) {{
                    setTimeout(() => {{
                        currentIndex++;
                        updateDisplay();
                    }}, 300);
                }}
            }};

            function updateDisplay() {{
                container.textContent = getText(currentIndex);
                const active = classifications[currentIndex];
                
                // Reset all label styles
                const labels = Object.keys(customColors);
                labels.forEach(l => {{
                    const el = document.getElementById(
                        'label_btn_' + sessionId + '_' + l
                    );
                    if (el) {{
                        el.style.background = 'transparent';
                    }}
                }});

                if (active) {{
                    const el = document.getElementById(
                        'label_btn_' + sessionId + '_' + active
                    );
                    if (el) {{
                        el.style.background = customColors[active] + '22';
                    }}
                    container.style.borderLeft = '6px solid ' +
                        customColors[active];
                }} else {{
                    container.style.borderLeft = '2px solid #F3F4F6';
                }}

                counter.textContent = "Doc " + (currentIndex + 1) +
                    " / " + texts.length;
                
                btnPrev.disabled = currentIndex === 0;
                btnNext.disabled = currentIndex === texts.length - 1;
            }};

            btnPrev.onclick = () => {{
                if (currentIndex > 0) {{
                    currentIndex--;
                    updateDisplay();
                }}
            }};

            btnNext.onclick = () => {{
                if (currentIndex < texts.length - 1) {{
                    currentIndex++;
                    updateDisplay();
                }}
            }};

            document.getElementById('btnDownloadAll_' + sessionId).onclick =
            () => {{
                const data = texts.map((t, i) => ({{
                    text_index: i,
                    text_id: getId(i),
                    text: getText(i),
                    label: classifications[i] || null
                }}));
                const blob = new Blob(
                    [JSON.stringify(data, null, 2)],
                    {{type: 'application/json'}}
                );
                const url = URL.createObjectURL(blob);
                const now = new Date();
                const nowStr = now.toISOString().slice(0, 19).replace(/:/g, "-");
                const a = document.createElement('a');
                a.href = url;
                a.download = "classifications_" + nowStr + ".json";
                a.click();
                URL.revokeObjectURL(url);
            }};

            updateDisplay();
        }})();
        </script>
        """.format(
            self.session_id,
            json.dumps(self.texts),
            json.dumps(self.custom_colors)
        )

        display(HTML(main_html + js_code))
