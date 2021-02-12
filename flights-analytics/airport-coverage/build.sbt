ThisBuild / scalaVersion := "2.12.12"
ThisBuild / organization := "com.flightaware.spark"

val sparkVersion = "3.0.1"

lazy val airportcoverage = (project in file("."))
  .settings(
    name := "AirportCoverage",
    libraryDependencies += "org.apache.spark" %% "spark-core" % sparkVersion,
    libraryDependencies += "org.apache.spark" %% "spark-sql" % sparkVersion,
    libraryDependencies += "org.scalatest" %% "scalatest" % "3.2.5" % Test,
  )

