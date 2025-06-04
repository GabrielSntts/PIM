function toggleMenu() {
  // Rolamento dos botões
  const menu = document.getElementById("mobilemenu")
  menu.classList.toggle("active")
}

document.querySelector("form").addEventListener("submit", function (e) {
  // Responsável por enviar a mensagem no campo
  e.preventDefault()

  const nome = document.getElementById("name").value.trim()
  const email = document.getElementById("email").value.trim()
  const mensagem = document.getElementById("message").value.trim()

  if (!nome || !email || !mensagem) {
    // Um "mini" validador, faz com que todos os campos tenham que estar completos
    alert(
      "Para enviar sua mensagem, complete todos os campos do formulário corretamente."
    )
    return
  }

  alert("Sua mensagem foi enviada com sucesso! Em breve entraremos em contato.")
  this.reset() // Isso apaga os campos para "enviar" uma nova mensagem
})

document.querySelectorAll('a[href^="#"]').forEach((link) => {
  // Animação leve do site quando você clica em "Projeto" ou outro campo
  link.addEventListener("click", function (e) {
    e.preventDefault()
    const target = document.querySelector(this.getAttribute("href"))
    if (target) {
      target.scrollIntoView({ behavior: "smooth" })
    }
  })
})

const observer = new IntersectionObserver((entries) => {
  // a animação do aparecimento dos elementos do "serviço" e "projetos"
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add("show")
    }
  })
}) // Foi codado para essa animação ser feita somente uma vez, porém vou alterar isso depois

document.querySelectorAll(".service-card, .project-card").forEach((el) => {
  el.classList.add("hidden")
  observer.observe(el)
})
