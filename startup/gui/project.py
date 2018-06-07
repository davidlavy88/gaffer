##########################################################################
#
#  Copyright (c) 2013-2014, Image Engine Design Inc. All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#      * Redistributions of source code must retain the above
#        copyright notice, this list of conditions and the following
#        disclaimer.
#
#      * Redistributions in binary form must reproduce the above
#        copyright notice, this list of conditions and the following
#        disclaimer in the documentation and/or other materials provided with
#        the distribution.
#
#      * Neither the name of John Haddon nor the names of
#        any other contributors to this software may be used to endorse or
#        promote products derived from this software without specific prior
#        written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
#  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
#  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
##########################################################################

import os
import functools

import IECore

import Gaffer
import GafferImage
import GafferUI
import GafferDispatch

##########################################################################
# Note this file is shared with the `dispatch` app. We need to ensure any
# changes here have the desired behaviour in both applications.
##########################################################################

##########################################################################
# Project variables
##########################################################################

def __scriptAdded( container, script ) :

	variables = script["variables"]
	if "projectName" not in variables :
		projectName = variables.addMember( "project:name", IECore.StringData( "default" ), "projectName" )
	if "projectRootDirectory" not in variables :
		projectRoot = variables.addMember( "project:rootDirectory", IECore.StringData( "$HOME/gaffer/projects/${project:name}" ), "projectRootDirectory" )

	Gaffer.MetadataAlgo.setReadOnly( variables["projectName"]["name"], True )
	Gaffer.MetadataAlgo.setReadOnly( variables["projectRootDirectory"]["name"], True )

	GafferImage.FormatPlug.acquireDefaultFormatPlug( script )

application.root()["scripts"].childAddedSignal().connect( __scriptAdded, scoped = False )

##########################################################################
# Bookmarks
##########################################################################

def __projectBookmark( widget, location ) :

	script = None
	while widget is not None :
		if hasattr( widget, "scriptNode" ) :
			script = widget.scriptNode()
			if isinstance( script, Gaffer.ScriptNode ) :
				break
		widget = widget.parent()

	if script is not None :
		p = script.context().substitute( location )
		if not os.path.exists( p ) :
			try :
				os.makedirs( p )
			except OSError :
				pass
		return p
	else :
		return os.getcwd()

GafferUI.Bookmarks.acquire( application ).add( "Project", functools.partial( __projectBookmark, location="${project:rootDirectory}" ) )
GafferUI.Bookmarks.acquire( application, category="script" ).setDefault( functools.partial( __projectBookmark, location="${project:rootDirectory}/scripts" ) )
GafferUI.Bookmarks.acquire( application, category="reference" ).setDefault( functools.partial( __projectBookmark, location="${project:rootDirectory}/references" ) )

##########################################################################
# Dispatchers
##########################################################################

dispatchers = [ GafferDispatch.LocalDispatcher ]
with IECore.IgnoredExceptions( ImportError ) :
	import GafferTractor
	dispatchers.append( GafferTractor.TractorDispatcher )

for dispatcher in dispatchers :

	Gaffer.Metadata.registerPlugValue( dispatcher, "jobName", "userDefault", "${script:name}" )
	directoryName = dispatcher.staticTypeName().rpartition( ":" )[2].replace( "Dispatcher", "" ).lower()
	Gaffer.Metadata.registerPlugValue( dispatcher, "jobsDirectory", "userDefault", "${project:rootDirectory}/dispatcher/" + directoryName )
