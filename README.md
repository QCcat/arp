# arp
<h2>Linux alias redactor</h2>

The code enables users to create, remove, and list aliases in Bash.

<br><br>

The new function appends the new alias to the existing aliases and writes the command to the Bashrc file 

	 arp new <alias name> <command>
      
The list function lists the aliases from the Bashrc file. 

	 arp list
      
The remove function deletes the specified alias. 

	 arp remove <alias name>
      
The default function sets the default functionality of Bashrc file. 

	arp default
  
The help function shows the help guide for the available commands. 

	arp help
<br><br>  
 <h2>install arp globally</h2>
 
	arp init
      
Important! when moving the executable file to another directory, the arp command will not be executed
<br><br>
<h2>Warning!</h2>
Don't use aliases with less than 3 values.
Don't try to remove an alias from less than 3 values! 
This will lead to undesirable consequences.
