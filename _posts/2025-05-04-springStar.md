---
layout: default
title:  "Spring Star"
date: 2025-05-04
category: group
tags: Godot Blender
permalink: springStar
excerpt: "An alien named Mweep crashes on a strange planet, leaving their spaceship broken and scattered everywhere. Fortunately, their escape capsule is equipped with a mobility device to navigate terrain safely: a spring. Your goal is to help Mweep traverse the hostile and surprisingly platformer-oriented geography of the planet to recover all of the parts of their spaceship to repair it and get off the planet. In your travels, you may encounter upgrades to your spring as well, which you will need to reach every part. Try to get Mweep back before dinner!"
---

<html lang="en">
  <head>
    <!-- Recommended meta tags -->
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1.0">
    <!--CSS-->
    <link rel="stylesheet" type="text/css" href="../stylesheets/default.css">
    <link rel="stylesheet" href="../stylesheets/posts.css">
  </head>
  <body>
    <!--Post intro-->
    <div class="section" style="background: var(--color-bg2-gradient); box-shadow: var(--shadow);">
      <h1 style="margin-bottom: 5px;">{{ page.title }}</h1>
      <div class="tags">
        {% for tag in page.tags %}
          <span class="tag">{{ tag }}</span>
          <div style="width: 10px;"></div>
        {% endfor %}
      </div>
      <div class="tags"> <!--Dates-->
        <span style="flex: 1; font-size: 12pt; text-align: right; font-weight: bold;">Last updated: {{ page.date | date: "%Y %B %-d" }}</span>
      </div>

      <p>
        {{ page.excerpt }}
      </p>

      <p>
        This game demo was created as part of a group project for a class. Through collaboration and teamwork, three classmates and I were able to complete a playable tutorial level and a rough, open hub location. The team and I were assigned leads to each aspect of the game. I was the lead of assets. My defined responsibilities were to create and design 3D models for the game environments and character, produce 2D textures for the models, organize the assets and other game files in a sensible order, and add proper lighting and camera effects. Throughout the course of four months, my greatest contributions to the game include creating a finished version of the character, Mweep, modeling the spring and capsule vehicle, and modeling the gas station and mechanic shop located in the hub.
      </p>

      <p>
        Although this game was formed as a school project for a semester-long class, it was treated as professional work, with paperwork and documentation that could be seen in a real-world company-run project. Along with the production of the game, we as a team had to provide a team contract, form a game design document and production timeline, and adhere to agile-style tasks. The class also required quarterly presentations that would update everyone on the current progress of our game, detailing the tasks we completed and our goals for the next quarter. With the presentations, we would take in feedback from the professor and other students to ensure the game stays on track. I also had the game playtested by peers, both in and out of the classroom, to get a fresh perspective on the game and find any difficulties that we developers may have been blind to.
      </p>

      <p>
        Spring Star was publicly showcased twice on campus. The first presentation was at the Celebration of Creative Inquiry, in which only our group and one other group from the game development class had the opportunity to showcase and receive feedback on our game demos, among other students presenting their latest research and other academic and creative achievements. The other showcase was at the end of the semester, where the members of Gustavus were free to play all of the game demos created for that class. Throughout these showcases, our table always had at least a small group of people waiting to playtest our game. People of all ages and gaming experience expressed enjoyment towards the game and gave positive feedback. Our professor enjoyed our game so much, in fact, that he printed a design of our game logo onto t-shirts!
      </p>
      
      <div style="display: flex; padding-top: 30px;">
        <a href="https://soampbar.itch.io/spring-star" class="gitLink">Playable Demo</a>
        <a href="https://github.com/Althories/f-springstar" class="gitLink">Github Repository</a>
      </div>
    </div>

    <!--Contents-->
    <div class="section" style="background: var(--color-bg2-gradient); box-shadow: var(--shadow);">
      <h1>Gallery</h1>
      <img class="photo" src="/Portfolio/images/posts/springStar/titleScreen.webp" alt="Spring Star title screen" style="max-width: 80%; padding-bottom: 20px;">

      <div class="gallery">
        <div class="gallerySpacer"></div>
        <div class="galleryPhoto">
          <img class="photo" src="/Portfolio/images/posts/springStar/tutorial.webp">
          <p class="photoDescription">Start of tutorial level</p>
        </div>
        <div class="galleryPhoto">
          <img class="photo" src="/Portfolio/images/posts/springStar/map.webp">
          <p class="photoDescription">Map of tutorial level</p>
        </div>
        <div class="galleryPhoto">
          <img class="photo" src="/Portfolio/images/posts/springStar/charge.webp">
          <p class="photoDescription">Performing a charged jump</p>
        </div>
        <div class="galleryPhoto">
          <img class="photo" src="/Portfolio/images/posts/springStar/compass.webp">
          <p class="photoDescription">Locating a ship part with the compass</p>
        </div>
        <div class="galleryPhoto">
          <img class="photo" src="/Portfolio/images/posts/springStar/gasStation.webp">
          <p class="photoDescription">Mechanic shop in the hub</p>
        </div>
        <div class="gallerySpacer"></div>
      </div>

      <div style="display: flex;">
        <img class="photo standaloneImage" src="/Portfolio/images/posts/springStar/mweep.gif" alt="Rotating GIF of Mweep">
        <img class="photo standaloneImage" src="/Portfolio/images/posts/springStar/tshirt" alt="T-shirt with the Spring Star logo">
        <img class="photo standaloneImage" src="/Portfolio/images/posts/springStar/spring.gif" alt="Rotating GIF of the spring">
      </div>
      
    </div>
  </body>
</html>