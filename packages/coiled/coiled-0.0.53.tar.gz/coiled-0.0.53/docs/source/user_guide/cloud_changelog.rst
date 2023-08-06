.. cloud_changelog:

==========================
Coiled Cloud Release Notes
==========================

These release notes are related to updates for `cloud.coiled.io <https://cloud.coiled.io>`_.

13 October 2021
===============

Fixes
+++++

* Environment variables sent to the Cluster with the keyword argument 
  ``environ=`` are now being converted to strings, which fixes
  occasional failures when sending non-string values to the Cluster.

Enhancements
++++++++++++

* You can now use Coiled in your own GCP account. Please refer to the
  :doc:`backends_gcp` documentation.
* You can now use Coiled in your own Azure account. Please refer to the
  :doc:`backends_azure` documentation.
* You can now select a ``region`` or ``zone`` when launching clusters in GCP.
* You can now create software environments using Docker images stored in your
  private ECR (AWS), ACR (Azure) or GAR (GCP) container registries, in addition
  to Docker Hub and other registries, by calling 
  ``coiled.create_software_environment(container="<URI>")``.
* Coiled now collects statistical profiling data from your Dask clusters.
  This data is visualized as a flame graph on the Analytics page for
  individual clusters.
* You can now hide/show columns in the Clusters Dashboard. The options are: Id,
  Cluster Name, Created By, Status, Num Workers, Software Environment,
  Cost (current), Cost(total), Last Seen, Backend, Runtime, Spot/Preemptible.
* Improve log filtering for AWS when viewing logs in the Coiled UI.


Documentation
+++++++++++++

* Added a new example on using the :doc:`Dask Snowflake <examples/snowflake>`
  connector.
* Fix link to Coiled's privacy policy in the :doc:`security` page.
* Added new section in the :doc:`gpu` documentation to demonstrate the use how
  of GPUs with the Afar library to run remote commands.


28 September 2021
=================

Fixes
+++++

* Resolve error that was throwing an "Unable to stop cluster" error message in the Clusters
  Dashboard for users using the Azure backend.
* Fix issue with workers not being created when users create a new Cluster using the AWS backend.
* Resolve error that was causing Clusters to shut down immediately upon creation for users using the AWS backend.
* Fix issue that was causing the Cluster Dashboard table to show zero workers count even though the workers were
  created and connected to the scheduler.


Enhancements
++++++++++++

* Add label containing the instance name to notification when running ``coiled.get_notifications()``.


Documentation
+++++++++++++

* Fix typo in CLI command, documentation mentioned ``coiled inspect`` but the right command is ``coiled env inspect``.
* Update :doc:`teams` page to better explain the distinction between Accounts and Teams.
