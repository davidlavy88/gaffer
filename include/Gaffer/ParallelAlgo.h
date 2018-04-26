//////////////////////////////////////////////////////////////////////////
//
//  Copyright (c) 2018, Image Engine Design Inc. All rights reserved.
//
//  Redistribution and use in source and binary forms, with or without
//  modification, are permitted provided that the following conditions are
//  met:
//
//      * Redistributions of source code must retain the above
//        copyright notice, this list of conditions and the following
//        disclaimer.
//
//      * Redistributions in binary form must reproduce the above
//        copyright notice, this list of conditions and the following
//        disclaimer in the documentation and/or other materials provided with
//        the distribution.
//
//      * Neither the name of John Haddon nor the names of
//        any other contributors to this software may be used to endorse or
//        promote products derived from this software without specific prior
//        written permission.
//
//  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
//  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
//  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
//  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
//  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
//  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
//  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
//  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
//  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
//  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
//  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//
//////////////////////////////////////////////////////////////////////////

#ifndef GAFFER_PARALLELALGO_H
#define GAFFER_PARALLELALGO_H

#include "Gaffer/Export.h"

#include "boost/signals.hpp"

#include <functional>

namespace Gaffer
{

namespace ParallelAlgo
{

/// Runs the specified function asynchronously on the main UI thread.
///
/// > Note : This function does nothing unless the GafferUI module has
/// > been imported.
///
/// > Warning : If calling a member function, you _must_ guarantee that
/// > the class instance will still be alive when the member function is
/// > called. Typically this means binding `this` via a smart pointer.
typedef std::function<void ()> UIThreadFunction;
GAFFER_API void callOnUIThread( const UIThreadFunction &function );

/// Signal used to request the calling of a function on the UI thread.
/// We service these requests in GafferUI.EventLoop.py.
///
/// > Note : This is an implementation detail. It is only exposed to allow
/// > emulation of the UI in unit tests, and theoretically to allow an
/// > alternative UI framework to be connected.
typedef boost::signal<void ( UIThreadFunction )> CallOnUIThreadSignal;
GAFFER_API CallOnUIThreadSignal &callOnUIThreadSignal();

} // namespace ParallelAlgo

} // namespace Gaffer

#endif // GAFFER_PARALLELALGO_H
