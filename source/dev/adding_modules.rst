.. _adding_modules:

How to add an Audio Module
##########################

1. `Introduction <#introduction>`__

2. `Create the folder structure <#create-the-folder-structure>`__

3. `Create an API file <#create-an-api-file>`__

4. `Add the source code and CAPI Wrapper <#add-the-source-code-and-capi-wrapper>`__

5. `Create a build file <#create-a-build-file>`__

6. `Add entries to build the module <#add-entries-to-build-the-module>`__

7. `Build the module and import to ARC <#build-the-module-and-import-to-arc>`__ 

8. `Test the module <#test-the-module>`__

Introduction
------------

This guide will outline how to incorporate, build, and test an audio algorithm in audioreach-engine, in the form of a **module**, using these basic steps:

	.. figure:: images/adding_modules/adding_modules_workflow_diagram.png
			:figclass: fig-center

As noted in the workflow diagram above, this guide will show how to add a module with source code, or how to instead add a prebuilt ".a" binary file, which will be discussed in the section `Create a build file <#create-a-build-file>`__.

After building the module and adding it to a usecase graph using ARC, the updated ACDB and workspace files can be pushed to the "etc/acdbdata" folder on the device. For more information on how to use ARC (also known as QACT), please refer to the ARC user guide.

Before following these steps, there are a few prerequisites to keep in mind:

	* These steps are based on adding a module to the AudioReach yocto project, so it is required to create a local yocto build first. To learn how to do this, please refer to the Platform Reference Guide for your preferred platform (such as the :ref:`raspberry_pi4` setup instructions). A guide on how to build a standalone module outside of the audioreach-engine source tree will be added at a later date.
	* It might be helpful to learn some basic information about CMake and KConfig, though this is not required. 
	* This guide will also be referencing **h2xml**, which is created by Qualcomm. Some information on h2xml can be found `here <https://github.com/Audioreach/h2xml>`__.
	* Additionally, it may help to look over the `Example Gain <https://github.com/Audioreach/audioreach-engine/tree/master/modules/examples/gain>`__ module, which will be used as an example throughout this guide.

To learn how to build a module that is already included in the audioreach-engine project, please refer to Step 3 of the section `Add entries to build the module <#add-entries-to-build-the-module>`__.

**Note:** This guide will often refer to a "tmp" audioreach-engine folder that will be generated from compiling audioreach-engine, which will contain important files used in multiple steps of this guide. 
Because this guide is written based on audioreach-engine compiled using the yocto build system, the exact location of audioreach-engine build artificat may vary depending on the build system. 
For example, on the Raspberry Pi 4, this folder will be located in "<build_root>/build/tmp/work/cortexa7t2hf-neon-vfpv4-poky-linux-gnueabi/audioreach-engine/1.0+git/audioreach-engine-1.0+git".

Create the folder structure
---------------------------
* First, choose a location to create the module folder. Most of the current modules are found in the `modules <https://github.com/Audioreach/audioreach-engine/tree/master/modules>`__ folder, in one of two locations:
	
	* The "audio" folder contains audio encoders and decoders.
	* The "processing" folder contains audio processing modules.
* Below is the recommended folder structure for a module:

	* api: Contains the API file.
	* build: Contains the CMakeLists build file.
	* lib: Contains the header files/source code
	* capi: Contains the header files/source code for the CAPI wrapper.
	* bin (optional): Contains the binary file

Create an API file
------------------
* The API file will be used by AudioReach Creator to obtain information about the module, such as configurable structs and parameters, the module description, and the module ID. An API file is required for every module.
	
	* For example, the below image shows some of the information included in the API file for the Example Gain module:
	
		.. figure:: images/adding_modules/3_api_module_entry_example_gain.png
			:figclass: fig-center
			:scale: 80 %

* When a module is compiled, the API will be converted to an XML file using h2xml. This XML file can then be imported into ARC, which will use this to obtain the module information. After this, the module will be available to use in ARC.
* For example, the API file will be used to construct the "Calibration Window" for a module, which can be viewed by double-clicking a module in the workspace of ARC. The Calibration Window is used to set configurable parameters for the module.
* To better visualize how the Calibration Window is constructed from the a module's API file, please note the image of API file for the Example Gain module below:

	.. figure:: images/adding_modules/1_api_example_gain.png
		:figclass: fig-center
		:scale: 80 %
		
	* This section of the API file depicts the parameter **PARAM_ID_GAIN_MODULE_GAIN**, as well as the struct **param_id_module_gain_cfg_t** that contains the variables **gain** and **reserved**. Additionally, underneath the parameters, there are some h2xml annotations.
	* These parameters, structs, and h2xml entries in the API file will be used by ARC to construct the Calibration Window for the Example Gain module, shown below:
	
	.. figure:: images/adding_modules/2_calibration_window_example_gain.png
		:figclass: fig-center
		:scale: 80 %

	* The image above shows the **PARAM_ID_GAIN_MODULE_GAIN** parameter with two configurable variables, **gain** and **reserved**. This reflects the **param_id_module_gain_cfg_t** struct in the API file. However, the name of the struct is not shown in ARC; it is only used internally in the API file to define the configurable variables. Instead, the parameter name will be shown.
	* The h2xml annotations are used to populate additional information such as the descriptions and the default values.

		* For example, the **gain** variable has a default value of "0x2000", which is shown in the h2xml annotations in the above section of the API.
		* Additionally, hovering the mouse over the **gain** variable in the Calibration Window will show the h2xml description for the variable.
* For a comprehensive overview on how to develop an API file, please refer to the "Module" section of the :ref:`capi_mod_dev_guide`.


Add the source code and CAPI Wrapper
------------------------------------
* The custom algorithm for the module can be developed and optimized using standard industrial tool such as Matlab.
* When developing the CAPI wrapper, there are a few functions that are mandatory to implement, including the entry point init functions, get_param, set_param, set_properties, get_properties, process, and end function. 
  For example, below is the list of the required CAPI functions from the Example Gain module:

	.. code-block:: bash

		static capi_vtbl_t vtbl = {capi_example_gain_module_process, capi_example_gain_module_end,
                                   capi_example_gain_module_set_param, capi_example_gain_module_get_param,
                                   capi_example_gain_module_set_properties, capi_example_gain_module_get_properties };

* For information on how to create a CAPI wrapper for the module, please refer to the :ref:`capi_mod_dev_guide`.
	
Create a build file
-------------------
* First, create a "CMakeLists.txt" file under the module's "build" directory. Please refer to the existing build files, such as the `Example Gain <https://github.com/Audioreach/audioreach-engine/blob/master/modules/examples/gain/CMakeLists.txt>`__.

	* If using a prebuilt binary file instead of the source files, please refer to the build file for the `iir_mbdrc <https://github.com/Audioreach/audioreach-engine/tree/master/modules/processing/gain_control/iir_mbdrc/build>`__ module.
* In the build file, add the "sources" and "includes" sections to link the module's source and header files. The layout of the "sources" and "includes" section should follow the below format:
	
	.. code-block:: bash

			set(module_name_sources
				{LIB_ROOT}/capi/src/<file1>.*
				{LIB_ROOT}/lib/src/<file2>.*
				{LIB_ROOT}/lib/src/<file3>.*
				....
			)
				
			set(module_name_includes
				{LIB_ROOT}/capi/inc
				{LIB_ROOT}/lib/inc
				....
			)

	* Note: If using a binary file, the "sources" section is not required.

* Now add the "spf_module_sources" section. This will be used by the AMDB, which stands for Audio Module DataBase. The AMDB will look for the CAPI entry point functions of the modules when the audio graph is created. 
  As an example, here is the "spf_module_sources" section for the Example Gain module:
	
	.. figure:: images/adding_modules/5_example_gain_build_file.png
		:figclass: fig-center
		:scale: 100 %

* Please note that all of the entries shown in the above example are required. Most of this information will be taken from the API file. Here is a list of each entry and their use:

	* **KConfig:** This will be used in the KConfig file to indicate whether the module will be automatically generated or not. 
	* **Name:** The name of the module.
	* **Major/minor version:** Major or minor version of the module.
	* **amdb_itype:** Interface type of the module. Currently only "capi" value is supported.
	* **amdb_mtype:** This is the module type. For example, in this case "PP" stands for post-processing or pre-processing. The other possible types include "end_point", "generic", "decoder", "encoder", "packetizer", "depacketizer", "converter", "detector", "generator", and "framework".
	* **amdb_mid:** This is the module ID. This module ID should be the same as the module ID in the API file.
	* **amdb_tag:** This tag will provide the prefix of the CAPI entry point functions for the module. In the Example Gain module shown above, the CAPI functions are prepended with "capi_example_gain". AMDB will use the prefix to find the entry functions; for example, "capi_example_gain_init".
	* **amdb_mod_name:** The name of the module. This should be the same name that is in the API file.
	* **srcs/includes:** These will link the sources and includes added in the build file. If you are using a binary, you do not need the "srcs" section.
	* **h2xml_headers:** The path to the API file
	* **CFlags:** Any CFlags that are required to build the module.

* Additionally, the **STATIC_LIB_PATH** entry is added in the case of using a binary file. This should follow the below format:

	.. code-block:: bash

		STATIC_LIB_PATH "[path_to_binary_file]/module_name.a"

Add entries to build the module
-------------------------------
* To ensure the module is compiled, it is required to add a few build entries in other audioreach-engine build files. Follow the below steps before building the module:

	1. In "audioreach-engine/modules/CMakeLists.txt", add the below entry (please note that this CONFIG_MODULE_NAME must be the same name that is in the module's build file, under the KConfig entry):
	
		.. code-block:: bash

			if(CONFIG_MODULE_NAME)
				add_subdirectory([path_to_module_cmake_file])
			endif()

	2. In "audioreach-engine/modules/KConfig", add an entry like below:

		.. code-block:: bash

			config MODULE_NAME
				tristate "Enable MODULE_NAME library"
				default n

	3. In "audioreach-engine/arch/<platform>/configs/defconfig", add an entry for the module in the format "CONFIG_MODULE_NAME". This must be the same name that is added to the modules/CMakeLists.txt file above. There are three options for setting the module entry:
	   
		* "y" will link the module to the audioreach-engine library in a single shared library.
		* "m" will build the module as a standalone shared library in the "tmp" audioreach-engine folder.
		* "n" will not build the module at all.

	* Note: To build a module that is already included in the opensource project, find the relevant entry for the module and set it to one of the above options. The modules that are present in the default
	  usecase graph will already be set to "y". Additionally, please make sure to also compile any dependencies for the module, which can be found in the :ref:`available_modules` list. For information
	  on how to test the module, please see the steps below.

Build the module and import to ARC
-----------------------------------
* Now all of the setup is completed. If using a yocto build, running "bitbake audioreach-engine" should build the module.

	* To ensure that the module was picked up for compilation after running the bitbake command, check the file "audioreach-engine/fwk/spf/amdb/autogen/linux/spf_static_build_config.h". The CAPI wrapper entry functions for the module should be printed here. If not, double check that the previous step was fully completed.

* When the module is compiled, h2xml will convert the API to the XML file that will be imported into ARC. This can be found in the "tmp" audioreach-engine folder, inside the folder "h2xml_autogen". This XML file will have the same name as the API file for the module.
* To use the module in an audio usecase graph, import the XML file into ARC. For steps on how to do this, please refer to section 4.1 of the ARC guide.

Test the module
-------------------
* First, set up the preferred device. A full device image can be generated from the yocto build and flashed after successfully compiling "audioreach-engine" and then generating a full image by running "bitbake <image_name>".
* If an image is already flashed onto the device, it is possible to use the module without re-flashing the image:

	* If the module entry was set to "y" in defconfig, simply push "libspf.so" to the "/usr/lib" folder on the device.
	
		* "libspf.so" is the audioreach-engine library, and it can be found in the "tmp" audioreach-engine folder.
	* If the module entry was set to "m", navigate to the "tmp" audioreach-engine and find the folder generated for the custom module. Here, there should be a ".so" file generated for the module. Push this to the "/usr/lib" folder on the device.
* Add the module to the audio usecase graph in ARC. Save the workspace to update the ACDB files.
* Push the updated ACDB files to the ACDB folder on the device and try running an audio use case. If there are no issues with the use case, the module will appear in the graph when ARC is connected to the device in online mode.

	* Please refer to the relevant :ref:`Platform Reference Guide` for steps on connecting ARC in online mode.
