
    const initialResume = "Built a Python data pipeline with pandas and PostgreSQL. Added unit tests with pytest and documented setup in Git.";
    const initialJob = "Junior Data Engineer\nRequired skills:\n- Python\n- SQL\n- PostgreSQL\nPreferred:\n- AWS\n- Docker";
    const sampleDraft = "Built a Python data pipeline using pandas and PostgreSQL. Added pytest unit tests and documented the setup in Git.";
    const terms = ["Python", "SQL", "PostgreSQL", "pandas", "AWS", "Docker", "Git", "Unit testing"];
    const aliases = {"Unit testing":["unit tests","unit testing","pytest"],"PostgreSQL":["postgresql","postgres"],"pandas":["pandas"],"Python":["python"],"SQL":["sql"],"AWS":["aws","amazon web services"],"Docker":["docker"],"Git":["git"]};
    let currentTab = "skills";
    let lastAnalysis = null;
    const $ = id => document.getElementById(id);
    function hasTerm(text, name) { return aliases[name].some(alias => new RegExp("(^|[^\\w])" + alias + "([^\\w]|$)","i").test(text)); }
    function requirements(job) {
      const required = [], preferred = [];
      let group = required;
      for (const line of job.split(/\r?\n/)) {
        if (/preferred|nice to have|bonus|optional/i.test(line)) group = preferred;
        else if (/required|must have|qualifications/i.test(line)) group = required;
        for (const term of terms) if (hasTerm(line, term) && !group.includes(term)) group.push(term);
      }
      return {required,preferred};
    }
    function wordSimilarity(a,b) {
      const tokenize = text => text.toLowerCase().match(/[a-z0-9+#.]+/g)?.filter(w => w.length > 1 && !["the","and","with","for","you","your","this","that","from","are","can","one","was","have","has","will","into","not","but","its","job","role"].includes(w)) || [];
      const x=tokenize(a), y=tokenize(b), vocab=[...new Set([...x,...y])];
      if (!x.length || !y.length || !vocab.length) return 0;
      const xv=vocab.map(w=>x.filter(t=>t===w).length), yv=vocab.map(w=>y.filter(t=>t===w).length);
      const dot=xv.reduce((s,v,i)=>s+v*yv[i],0), nx=Math.sqrt(xv.reduce((s,v)=>s+v*v,0)), ny=Math.sqrt(yv.reduce((s,v)=>s+v*v,0));
      return nx&&ny ? dot/(nx*ny) : 0;
    }
    function analyze(resume, job) {
      const groups=requirements(job), found=terms.filter(t=>hasTerm(resume,t));
      const req=groups.required.length ? found.filter(t=>groups.required.includes(t)).length/groups.required.length : 0;
      const pref=groups.preferred.length ? found.filter(t=>groups.preferred.includes(t)).length/groups.preferred.length : 0;
      const sim=wordSimilarity(resume,job), score=Math.round(100*(.60*req+.15*pref+.25*sim));
      return {groups,found,gaps:[...groups.required,...groups.preferred].filter(t=>!found.includes(t)),req:Math.round(req*100),pref:Math.round(pref*100),sim:Math.round(sim*100),score};
    }
    function renderResult() {
      const resume=$("resumeInput").value.trim(), job=$("jobInput").value.trim();
      const r=analyze(resume,job); lastAnalysis=r;
      const title=job.split(/\r?\n/)[0].trim() || "Target role";
      $("roleLabel").textContent=title;
      $("scoreValue").textContent=r.score;
      $("scoreRing").style.background=`conic-gradient(var(--green) 0deg ${r.score*3.6}deg, #e7ede6 ${r.score*3.6}deg 360deg)`;
      $("scoreHeadline").textContent=r.score>=75?"Strong document alignment":r.score>=50?"Some relevant evidence found":"A few role signals are missing";
      $("scoreSubhead").textContent=`${r.found.length} relevant terms detected · ${r.gaps.length} not detected in the current text`;
      [["required",r.req],["preferred",r.pref],["similarity",r.sim]].forEach(([k,v])=>{$(`${k}Value`).textContent=`${v}%`;$(`${k}Bar`).style.width=`${v}%`});
      $("upgradeCard").classList.remove("show");
      renderTab();
    }
    function renderTab() {
      if (!lastAnalysis) return;
      const r=lastAnalysis, box=$("tabContent");
      if(currentTab==="skills") {
        const matched=r.found.filter(t=>[...r.groups.required,...r.groups.preferred].includes(t));
        box.innerHTML=`<div style="margin-bottom:8px;color:#748178;font-weight:700">Detected in resume</div><div class="skill-list">${matched.map(t=>`<span class="skill">${t} · found</span>`).join("")||"<span>No listed skills detected yet.</span>"}${r.gaps.map(t=>`<span class="skill miss">${t} · not detected</span>`).join("")}</div>`;
      } else if(currentTab==="evidence") {
        const evidence=r.found.map(t=>`<b>${t}</b>`).join(", ");
        box.innerHTML=`<div style="color:#748178;font-weight:700;margin-bottom:7px">Text evidence found</div><div>${evidence?`Your resume contains terms such as ${evidence}. Review the original sentences to confirm they describe your own work.`:"No supported terms were found in the text. Try the synthetic sample or add the exact wording from your real experience."}</div>`;
      } else {
        const recommendation=r.gaps.length?`If you have used ${r.gaps.slice(0,3).join(", ")}, add a concrete project or coursework example. If not, build evidence before listing those skills.`:"Your listed skills are detected. Check that each one has a specific example behind it.";
        box.innerHTML=`<div style="color:#748178;font-weight:700;margin-bottom:7px">A grounded next step</div><div>${recommendation}<br><br><button class="btn" id="rewriteBtn" type="button" style="min-height:34px;padding:0 11px;font-size:9px">Preview a synthetic rewrite <span aria-hidden="true">✦</span></button></div>`;
        $("rewriteBtn").addEventListener("click", previewRewrite);
      }
    }
    function previewRewrite() {
      const sameSample=$("resumeInput").value.trim()===initialResume;
      const draft=sameSample?sampleDraft:$("resumeInput").value.trim();
      const after=analyze(draft,$("jobInput").value.trim());
      $("draftCopy").textContent=sameSample?`“${sampleDraft}” This sample edit improves clarity and keeps the original facts intact.`:"For this custom text, no AI call is made. The full app can create an opt-in draft with your own Groq API key; review every claim before using it.";
      $("afterScore").textContent=sameSample?`After · ${after.score} / 100`:"AI draft available in full app";
      $("upgradeCard").classList.add("show");
    }
    $("analyzeBtn").addEventListener("click",renderResult);
    document.querySelectorAll(".tab-btn").forEach(button=>button.addEventListener("click",()=>{currentTab=button.dataset.tab;document.querySelectorAll(".tab-btn").forEach(b=>b.setAttribute("aria-selected",b===button?"true":"false"));renderTab()}));
    $("resumeInput").addEventListener("input",()=>{$("upgradeCard").classList.remove("show")});
    $("jobInput").addEventListener("input",()=>{$("upgradeCard").classList.remove("show")});
    $("year").textContent=new Date().getFullYear();
    renderResult();
  