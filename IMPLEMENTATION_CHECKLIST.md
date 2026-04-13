# Master Volume Implementation Checklist

> Cross-reference of all 4 Parts (23 chapters, 866 articles) against Python `@maxwell_cite` implementations.
> Generated from scanning every `.py` file in `maxwell/` for `@maxwell_cite` decorators.

---

## VOLUME 1

### PART I — ELECTROSTATICS (Arts. 1-229)

**Preliminary: On the Measurement of Quantities (Arts. 1-26)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 1 | Expression of a quantity | YES |
| 2 | Dimensions of derived units | |
| 3-5 | Fundamental units | |
| 6 | Derived units | |
| 7 | Physical continuity | |
| 8 | Discontinuity | |
| 9 | Periodic functions | |
| 10 | Physical quantities & space | |
| 11 | Scalar and Vector | |
| 12 | Forces and Fluxes | |
| 13 | Corresponding vectors | |
| 14 | Line/surface integration | |
| 15 | Longitudinal/rotational | |
| 16 | Line-integrals/potentials | |
| 17 | Hamilton's expression | |
| 18 | Cyclic regions | |
| 19 | Acyclic region potential | |
| 20 | Cyclic region potential | |
| 21 | Surface-integrals | |
| 22 | Surfaces/tubes of flow | |
| 23 | Right/left-handed relations | |
| 24 | Line→surface integral transform | |
| 25 | Hamilton ∇ operation | |
| 26 | ∇² operation | |

**Ch I: Description of Phenomena (Arts. 27-62)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 27 | Electrification by friction | |
| 28 | Electrification by induction | |
| 29 | Conduction. Conductors/insulators | YES |
| 30 | Equal positive/negative | YES |
| 31 | Charge vessel opposite | |
| 32 | Discharge into metallic vessel | |
| 33 | Gold-leaf electroscope | |
| 34 | Electricity as measurable | |
| 35 | Electricity as physical quantity | |
| 36 | Two fluids theory | |
| 37 | One fluid theory | |
| 38 | Force measurement | YES |
| 39 | Force-quantity relation | YES |
| 40 | Force-distance variation | YES |
| 41,42 | Electrostatic unit | YES |
| 43 | Proof of inverse square | YES |
| 44 | Electric field | YES |
| 45 | EMF and potential | YES |
| 46 | Equipotential surfaces | YES |
| 47 | Lines of force | YES |
| 48 | Electric tension | |
| 49 | Electromotive force | |
| 50 | Capacity/Accumulators | |
| 51 | Resistance | |
| 52 | Specific inductive capacity | |
| 53 | Absorption of electricity | |
| 54 | Impossibility of absolute charge | |
| 55-57 | Disruptive discharge | |
| 58 | Tourmaline phenomena | |
| 59 | Plan of treatise | |
| 60 | Electric polarization/displacement | |
| 61 | Incompressible fluid analogy | |
| 62 | Peculiarities of theory | |

**Ch II: Elementary Mathematical Theory (Arts. 63-83)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 63 | Electricity as mathematical | |
| 64 | Volume/surface/line density | |
| 65 | Electrostatic unit definition | |
| 66 | Law of force | YES |
| 67 | Resultant force | YES |
| 68 | Resultant intensity | YES |
| 69 | Line-integral/EMF | YES |
| 70 | Electric potential | YES |
| 71 | Resultant from potential | YES |
| 72 | Conductor potential uniform | |
| 73 | Potential of system | YES |
| 74a-e | Inverse square proof (Cavendish) | YES |
| 75 | Surface-integral of induction | YES |
| 76 | Induction through closed surface | YES |
| 77 | Poisson/Laplace equation | YES |
| 78a-c | Surface conditions | YES |
| 79 | Force on electrified surface | |
| 80 | Charge on surface only | |
| 81 | Line/point distribution impossible | |
| 82 | Lines of electric induction | YES |
| 83a-b | Specific inductive capacity | YES |

**Ch III: Electrical Work & Energy (Arts. 84-94)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 84 | Superposition/energy | YES |
| 85a | Energy change | YES |
| 85b | Potential-charge relations | YES |
| 86 | Reciprocity theorems | |
| 87 | Coefficients of potential/capacity | |
| 88 | Dimensions of coefficients | |
| 89a-e | Coefficient relations | |
| 90a-b | Approximate coefficients | |
| 91-93c | Force/work expressions | |
| 94 | System comparison | |

**Ch IV: General Theorems (Arts. 95-102)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 95a-b | Two methods | |
| 96a-d | Green's Theorem | |
| 97a-b | Green's method applications | |
| 98 | Green's Function | |
| 99a-b | Energy as volume integral | |
| 100a-e | Thomson's Theorem | |
| 101a-h | Energy with dielectric constants | |
| 102a-c | Limiting values | |

**Ch V: Mechanical Action (Arts. 103-111)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 103 | Force from potentials | |
| 104 | Force from combined potential | |
| 105 | Stress in medium | |
| 106 | Stress type | |
| 107 | Surface modification | |
| 108 | Integral over all space | |
| 109 | Faraday's tension/pressure | |
| 110 | Stress in fluid objections | |
| 111 | Electric polarization theory | |

**Ch VI: Points & Lines of Equilibrium (Arts. 112-116)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 112 | Equilibrium conditions | |
| 113 | Number of equilibrium points | |
| 114 | Conical point/self-intersection | |
| 115 | Equipotential intersection angles | |
| 116 | Unstable equilibrium | |

**Ch VII: Equipotential Surfaces (Arts. 117-123)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 117 | Practical importance | |
| 118 | Two points 4:1 | |
| 119 | Two points 4:-1 | |
| 120 | Point in uniform field | |
| 121 | Three points | |
| 122 | Faraday's lines of force | |
| 123 | Diagram method | |

**Ch VIII: Simple Cases (Arts. 124-127)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 124 | Two parallel planes | |
| 125 | Concentric spheres | |
| 126 | Coaxial cylinders | |
| 127 | Longitudinal force on cylinder | |

**Ch IX: Spherical Harmonics (Arts. 128-146)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 128-146 | Spherical harmonics | |

**Ch X: Confocal Surfaces (Arts. 147-154)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 147-154 | Confocal quadrics | |

**Ch XI: Electric Images (Arts. 155-181)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 155-181 | Electric images | |

**Ch XII: Conjugate Functions 2D (Arts. 182-206)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 182-206 | Conjugate functions | |

**Ch XIII: Electrostatic Instruments (Arts. 207-229)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 207-229 | Instruments | |

**PART I TOTAL: 28/229 articles implemented (12%)**

---

### PART II — ELECTROKINEMATICS (Arts. 230-370)

**Ch I: Electric Current (Arts. 230-240)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 230-240 | Electric current phenomena | |

**Ch II: Conduction & Resistance (Arts. 241-245)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 241 | Ohm's Law | YES |
| 242 | Joule's Law | |
| 243 | Heat analogy | YES |
| 244 | Differences | YES |
| 245 | Faraday's doctrine | YES |

**Ch III: EMF Between Bodies (Arts. 246-248)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 246-248 | Contact EMF | |

**Ch IV: Electrolysis (Arts. 249-263)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 249-263 | Electrolysis | |

**Ch V: Electrolytic Polarization (Arts. 264-272)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 264-272 | Polarization | |

**Ch VI: Mathematical Theory of Currents (Arts. 273-284)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 273-276 | Linear conductors | |
| 277 | Resistance uniform section | YES |
| 278 | Dimensions in Ohm's law | YES |
| 279 | Specific resistance EMU | YES |
| 280-284 | Linear systems | |

**Ch VII: Conduction 3D (Arts. 285-296)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 285-296 | 3D conduction | |

**Ch VIII: Resistance 3D (Arts. 297-309)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 297-309 | 3D resistance | |

**Ch IX: Heterogeneous Media (Arts. 310-324)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 310-324 | Heterogeneous conduction | |

**Ch X: Conduction in Dielectrics (Arts. 325-334)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 325-334 | Dielectric conduction | |

**Ch XI: Resistance Measurement (Arts. 335-358)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 335-358 | Resistance measurement | |

**Ch XII: Resistance of Substances (Arts. 359-370)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 359-370 | Substance resistance | |

**PART II TOTAL: 4/141 articles implemented (3%)**

---

## VOLUME 2

### PART III — MAGNETISM (Arts. 371-474)

**Ch I: Elementary Theory (Arts. 371-394)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 371-376 | Properties of magnets | |
| 377 | Equal opposite magnetism | YES |
| 378 | Breaking a magnet | YES |
| 379 | Built of magnetic particles | YES |
| 380 | Magnetic 'matter' theory | YES |
| 381 | Magnetization as vector | YES |
| 382 | Magnetic Polarization | YES |
| 383 | Magnetic particle properties | YES |
| 384 | Magnetic moment definitions | YES |
| 385 | Potential of magnetized element | YES |
| 386 | Potential finite size | |
| 387 | Particle-particle action | |
| 388 | Particular cases | |
| 389 | Potential energy in field | YES |
| 390 | Magnetic moment/axis | YES |
| 391 | Spherical harmonics expansion | |
| 392 | Centre/axes of magnet | |
| 393 | North/s pole conventions | YES |
| 394 | Direction of magnetic force | YES |

**Ch II: Magnetic Force & Induction (Arts. 395-406)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 395-398 | Magnetic force defined | |
| 399 | Thin disk / induction | YES |
| 400 | Force/induction/magnetization relation | |
| 401 | Line-integral of force | |
| 402 | Surface-integral of induction | |
| 403 | Solenoidal distribution | |
| 404 | Surfaces/tubes of induction | |
| 405 | Vector-potential of induction | YES |
| 406 | Scalar/vector potential relation | YES |

**Ch III: Magnetic Solenoids & Shells (Arts. 407-423)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 407-408 | Solenoid definitions | |
| 409 | Shell potential = strength × solid angle | YES |
| 410 | Another proof method | YES |
| 411 | Potential difference across shell | YES |
| 412 | Lamellar distribution | YES |
| 413 | Complex lamellar | YES |
| 414 | Solenoidal magnet potential | |
| 415 | Lamellar magnet potential | YES |
| 416 | Vector-potential of lamellar | YES |
| 417 | Solid angle of closed curve | YES |
| 418 | Solid angle as curve length | YES |
| 419 | Solid angle by two integrals | YES |
| 420 | Pi as determinant | YES |
| 421 | Cyclic function | YES |
| 422 | Vector-potential of closed curve | YES |
| 423 | Shell energy in field | |

**Ch IV: Induced Magnetization (Arts. 424-430)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 424-426 | Magnetic induction definition | |
| 427 | Poisson's method | YES |
| 428 | Faraday's method | YES |
| 429 | Body in magnetic medium | YES |
| 430 | Poisson's physical theory | |

**Ch V: Particular Problems (Arts. 431-441)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 431 | Hollow spherical shell | YES |
| 432 | Large kappa case | YES |
| 433 | i=1 case | YES |
| 434 | 2D corresponding case | YES |
| 435 | Anisotropic sphere | YES |
| 436 | Six coefficients | YES |
| 437 | Ellipsoid in uniform force | YES |
| 438 | Flat/long ellipsoids | YES |
| 439 | Neumann/Kirchhoff/Green | YES |
| 440 | Small kappa approximation | YES |
| 441 | Ship's magnetism | YES |

**Ch VI: Weber's Theory (Arts. 442-448)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 442 | Maximum magnetization | YES |
| 443 | Weber's temporary magnetization | YES |
| 444 | Residual magnetization | |
| 445 | Modified theory | |
| 446 | Demagnetization | |
| 447 | Dimensional effects | |
| 448 | Joule's experiments | |

**Ch VII: Magnetic Measurements (Arts. 449-464)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 449-464 | Measurement instruments | |

**Ch VIII: Terrestrial Magnetism (Arts. 465-474)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 465-474 | Earth's magnetic field | |

**PART III TOTAL: 46/104 articles implemented (44%)**

---

### PART IV — ELECTROMAGNETISM (Arts. 475-866)

**Ch I: Electromagnetic Force (Arts. 475-501)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 475 | Örsted's discovery | YES |
| 476 | Magnetic field near current | YES |
| 477 | Vertical current action | YES |
| 478 | Straight current force proof | YES |
| 479 | Electromagnetic measure | YES |
| 480 | Potential function | |
| 481 | Current vs magnetic shell | |
| 482 | Small circuit as magnet | |
| 483 | Closed circuit deduction | |
| 484 | Circuit vs shell comparison | |
| 485 | Magnetic potential of circuit | |
| 486 | Continuous rotation | |
| 487 | Equipotential surface form | |
| 488 | Magnet-circuit action | |
| 489 | Reaction on circuit | |
| 490 | Force on wire in field | YES |
| 491 | Electromagnetic rotations | YES |
| 492 | Circuit-circuit action | YES |
| 493 | Faraday's method | |
| 494 | Parallel currents illustration | YES |
| 495 | Current unit dimensions | |
| 496 | Wire urged from side | YES |
| 497 | Infinite current on coplanar | YES |
| 498 | Laws statement | |
| 499 | Generality of laws | |
| 500 | Force on circuit in field | |
| 501 | Force on conductor not current | YES |

**Ch II: Ampère's Investigation (Arts. 502-527)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 502-505 | Ampère's experiments | |
| 506 | Crooked conductor | |
| 507 | Third experiment | |
| 508 | Fourth experiment | |
| 509-521 | Ampère's analysis | |
| 522 | Quaternions | YES |
| 523-527 | Final expressions | |

**Ch III: Induction of Currents (Arts. 528-545)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 528 | Faraday's discovery | YES |
| 529 | Faraday's method | YES |
| 530 | Magneto-electric induction | YES |
| 531 | General induction law | YES |
| 532 | Direction of induced | |
| 533 | Earth induction | |
| 534 | Material independence | |
| 535 | No tendency to move conductor | |
| 536 | Felici's experiments | YES |
| 537 | Galvanometer integral | |
| 538 | Conjugate coil positions | |
| 539 | Mathematical expression | YES |
| 540 | Electrotonic state | |
| 541 | Lines of force | |
| 542 | Lenz's law/Neumann | |
| 543 | Helmholtz deduction | |
| 544 | Thomson's application | |
| 545 | Weber's contributions | |

**Ch IV: Self-Induction (Arts. 546-552)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 546 | Electromagnet shock | YES |
| 547 | Apparent momentum | YES |
| 548 | Water tube difference | YES |
| 549 | Not electricity momentum | YES |
| 550 | Momentum analogy | YES |
| 551 | Electro-kinetic energy | YES |
| 552 | Dynamical theory | |

**Ch V: Connected System Equations (Arts. 553-567)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 553-567 | Lagrange dynamics | |

**Ch VI: Dynamical Theory (Arts. 568-577)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 568-577 | Kinetic energy of currents | |

**Ch VII: Electric Circuits (Arts. 578-584)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 578 | Electrokinetic energy | YES |
| 579 | EMF in circuit | YES |
| 580 | Electromagnetic force | |
| 581 | Two circuits | YES |
| 582 | Induced currents | |
| 583 | Mechanical action | |
| 584 | Mutual potential | YES |

**Ch VIII: Secondary Circuit (Arts. 585-603)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 585 | Electrokinetic momentum | YES |
| 586 | Line-integral expression | YES |
| 587 | Contiguous circuits | YES |
| 588 | Surface-integral | YES |
| 589 | Crooked vs straight | YES |
| 590 | Momentum as vector | YES |
| 591 | Relation to induction (Eq A) | YES |
| 592 | Name justification | YES |
| 593 | Sign conventions | |
| 594 | Sliding piece | |
| 595 | EMF from motion | |
| 596 | Force on sliding piece | |
| 597 | Induction line definitions | |
| 598 | General EMF equations (B) | |
| 599 | EMF analysis | |
| 600 | Moving axes | |
| 601 | Potential with moving axes | |
| 602 | Force on conductor | |
| 603 | Force on element (Eq C) | |

**Ch IX: General Field Equations (Arts. 604-619)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 604 | Recapitulation | |
| 605 | Magnetization (Eq D) | |
| 606 | Force-current relation | |
| 607 | Currents (Eq E) | |
| 608 | Displacement (Eq F) | |
| 609 | Conductivity (Eq G) | |
| 610 | Total currents (Eq H) | |
| 611 | Currents from EMF (Eq I) | |
| 612 | Volume density (Eq J) | |
| 613 | Surface density (Eq K) | |
| 614 | Permeability (Eq L) | |
| 615 | Ampère's magnets | |
| 616 | Currents from momentum | YES |
| 617 | Vector-potential | YES |
| 618 | Quaternion expressions | |
| 619 | Quaternion equations | |

**Ch X: Dimensions of Units (Arts. 620-629)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 620-629 | Unit dimensions | YES |

**Ch XI: Energy & Stress (Arts. 630-646)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 630 | Electrostatic energy | YES |
| 631 | Energy from EMF/displacement | YES |
| 632 | Magnetic energy | YES |
| 633 | Magnetic energy squared | YES |
| 634 | Electrokinetic energy | YES |
| 635 | Energy from induction/force | |
| 636 | Method | |
| 637 | Energy comparison | |
| 638 | Magnetic→electrokinetic | YES |
| 639 | Force on magnetized particle | |
| 640 | Force from current | |
| 641 | Stress hypothesis | YES |
| 642 | Stress character | YES |
| 643 | Tension/pressure | YES |
| 644 | Force on conductor | |
| 645 | Faraday's stress theory | |
| 646 | Numerical tension | YES |

**Ch XII: Current-Sheets (Arts. 647-674)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 647-652 | Current-sheet theory | |
| 653 | Sheet potential | |
| 654 | Infinite conductivity | |
| 655 | Impervious sheet | |
| 656-674 | Various sheet configurations | |

**Ch XIII: Parallel Currents (Arts. 675-693)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 675 | Plane/spherical/ellipsoidal | YES |
| 676 | Solenoid | YES |
| 677 | Long solenoid | YES |
| 678 | End force | |
| 679 | Induction coils | |
| 680 | Wire thickness | |
| 681 | Endless solenoid | |
| 682 | Cylindrical conductors | YES |
| 683 | External action | YES |
| 684 | Vector-potential | YES |
| 685 | Kinetic energy | YES |
| 686 | Repulsion | YES |
| 687 | Ampère's tension | |
| 688 | Self-induction doubled wire | |
| 689 | Varying intensity | |
| 690 | EMF-total current relation | |
| 691 | Geometric mean distance | YES |
| 692 | Particular cases | YES |
| 693 | Insulated wire coil | |

**Ch XIV: Circular Currents (Arts. 694-706)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 694 | Spherical bowl potential | |
| 695 | Circle solid angle | |
| 696 | Two circles energy | |
| 697 | Coil couple moment | YES |
| 698 | P_i' values | |
| 699 | Parallel circle attraction | YES |
| 700 | Finite section coil | |
| 701 | Elliptic integrals | |
| 702 | Lines of force | YES |
| 703 | Differential equation | |
| 704-705 | Approximations | |
| 706 | Maximum self-induction | |

**Ch XV: Electromagnetic Instruments (Arts. 707-729)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 707-729 | Instruments | |

**Ch XVI: Observations (Arts. 730-751)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 730-751 | Observation methods | |

**Ch XVII: Coil Comparison (Arts. 752-761)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 752-761 | Coil comparison | |

**Ch XVIII: Resistance Unit (Arts. 758-767)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 758-767 | Resistance measurement | |

**Ch XIX: ESU vs EMU (Arts. 768-780)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 768-780 | Unit ratio | YES |

**Ch XX: EM Theory of Light (Arts. 781-805)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 781 | Medium comparison | YES |
| 782 | Energy during propagation | |
| 783 | Propagation equation | YES |
| 784 | Non-conductor solution | |
| 785 | Wave characteristics | |
| 786 | Propagation velocity | YES |
| 787 | Velocity vs light | YES |
| 788 | K = n² | YES |
| 789 | Paraffin comparison | |
| 790 | Plane wave theory | YES |
| 791 | Displacement perpendicular | YES |
| 792 | Energy/stress radiation | |
| 793 | Light pressure | |
| 794 | Crystallized medium | |
| 795 | Plane wave propagation | |
| 796 | Two waves | |
| 797 | Fresnel agreement | |
| 798 | Conductivity/opacity | |
| 799 | Facts comparison | |
| 800 | Transparent metals | |
| 801 | Conductor solution | |
| 802 | Infinite medium | |
| 803 | Diffusion characteristics | |
| 804 | Current start disturbance | |
| 805 | Ultimate state | |

**Ch XXI: Magnetic Action on Light (Arts. 806-831)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 806 | Magnetism-light forms | YES |
| 807 | Polarization rotation | YES |
| 808 | Phenomena laws | YES |
| 809 | Verdet's discovery | YES |
| 810 | Quartz rotation | YES |
| 811-831 | Kinematical analysis | |

**Ch XXII: Molecular Currents (Arts. 832-845)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 832-845 | Molecular current theory | |

**Ch XXIII: Action at Distance (Arts. 846-866)**
| Art | Title | Implemented |
|-----|-------|:-----------:|
| 846-856 | Action-at-distance theories | |
| 857 | Segregating force | YES |
| 858 | Moving conductors | YES |
| 859 | Gauss formula failure | YES |
| 860 | Weber formula agreement | |
| 861 | Gauss letter | |
| 862-864 | Riemann/Neumann/Betti | |
| 865 | Medium repugnance | YES |
| 866 | Medium necessity | YES |

**PART IV TOTAL: 215/392 articles implemented (55%)**

---

## OVERALL SUMMARY

| Part | Volume | Articles Range | Total Articles | Implemented | Coverage |
|------|--------|---------------|---------------|-------------|----------|
| I: Electrostatics | Vol 1 | 1-229 | 229 | 28 | 12% |
| II: Electrokinematics | Vol 1 | 230-370 | 141 | 4 | 3% |
| III: Magnetism | Vol 2 | 371-474 | 104 | 46 | 44% |
| IV: Electromagnetism | Vol 2 | 475-866 | 392 | 215 | 55% |
| **TOTAL** | | **1-866** | **866** | **293** | **34%** |

---

## MISSING ARTICLES BY PART (Top Priority Gaps)

### Part I (Electrostatics) — 201 articles missing
Key gaps: Ch III (Energy), Ch IV (Green's/Thomson), Ch V-XIII (most advanced topics)

### Part II (Electrokinematics) — 137 articles missing
Key gaps: Nearly all of Part II — current theory, electrolysis, 3D conduction, instruments

### Part III (Magnetism) — 58 articles missing
Key gaps: Ch I (elementary, partial), Ch VII (measurements), Ch VIII (terrestrial)

### Part IV (Electromagnetism) — 177 articles missing
Key gaps: Ch II (Ampère analysis), Ch V-VI (dynamics), Ch XII (current-sheets), Ch XV-XVIII (instruments/measurements), Ch XXII (molecular currents)
