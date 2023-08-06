/*
** The OpenGL Extension Wrangler Library
** Copyright (C) 2008-2017, Nigel Stewart <nigels[]users sourceforge net>
** Copyright (C) 2002-2008, Milan Ikits <milan ikits[]ieee org>
** Copyright (C) 2002-2008, Marcelo E. Magallon <mmagallo[]debian org>
** Copyright (C) 2002, Lev Povalahev
** All rights reserved.
** 
** Redistribution and use in source and binary forms, with or without 
** modification, are permitted provided that the following conditions are met:
** 
** * Redistributions of source code must retain the above copyright notice, 
**   this list of conditions and the following disclaimer.
** * Redistributions in binary form must reproduce the above copyright notice, 
**   this list of conditions and the following disclaimer in the documentation 
**   and/or other materials provided with the distribution.
** * The name of the author may be used to endorse or promote products 
**   derived from this software without specific prior written permission.
**
** THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
** AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
** IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
** ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE 
** LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
** CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
** SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
** INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
** CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
** ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
** THE POSSIBILITY OF SUCH DAMAGE.
*/
/*
 * Mesa 3-D graphics library
 * Version:  7.0
 *
 * Copyright (C) 1999-2007  Brian Paul   All Rights Reserved.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and associated documentation files (the "Software"),
 * to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included
 * in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
 * OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
 * BRIAN PAUL BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN
 * AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */
/*
** Copyright (c) 2007 The Khronos Group Inc.
** 
** Permission is hereby granted, free of charge, to any person obtaining a
** copy of this software and/or associated documentation files (the
** "Materials"), to deal in the Materials without restriction, including
** without limitation the rights to use, copy, modify, merge, publish,
** distribute, sublicense, and/or sell copies of the Materials, and to
** permit persons to whom the Materials are furnished to do so, subject to
** the following conditions:
** 
** The above copyright notice and this permission notice shall be included
** in all copies or substantial portions of the Materials.
** 
** THE MATERIALS ARE PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
** EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
** MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
** IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
,** CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
** TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
** MATERIALS OR THE USE OR OTHER DEALINGS IN THE MATERIALS.
*/
#ifndef __glew_h__
#define __glew_h__
#define __GLEW_H__
#if defined(__gl_h_) || defined(__GL_H__) || defined(_GL_H) || defined(__X_GL_H)
#error gl.h included before glew.h
#endif
#if defined(__gl2_h_)
#error gl2.h included before glew.h
#endif
#if defined(__gltypes_h_)
#error gltypes.h included before glew.h
#endif
#if defined(__REGAL_H__)
#error Regal.h included before glew.h
#endif
#if defined(__glext_h_) || defined(__GLEXT_H_) || defined(__gl_glext_h_)
#error glext.h included before glew.h
#endif
#if defined(__gl_ATI_h_)
#error glATI.h included before glew.h
#endif
#define __gl_h_
#define __gl2_h_
#define __GL_H__
#define _GL_H
#define __gltypes_h_
#define __REGAL_H__
#define __X_GL_H
#define __glext_h_
#define __gl_glext_h_
#define __GLEXT_H_
#define __gl_ATI_h_
#if defined(_WIN32)
/*
 * GLEW does not include <windows.h> to avoid name space pollution.
 * GL needs GLAPI and GLAPIENTRY, GLU needs APIENTRY, CALLBACK, and wchar_t
 * defined properly.
 */
/* <windef.h> and <gl.h>*/
#ifdef APIENTRY
#  ifndef GLAPIENTRY
#    define GLAPIENTRY APIENTRY
#  endif
#  ifndef GLEWAPIENTRY
#    define GLEWAPIENTRY APIENTRY
#  endif
#else
#define GLEW_APIENTRY_DEFINED
#  if defined(__MINGW32__) || defined(__CYGWIN__) || (_MSC_VER >= 800) || defined(_STDCALL_SUPPORTED) || defined(__BORLANDC__)
#    define APIENTRY __stdcall
#    ifndef GLAPIENTRY
#      define GLAPIENTRY __stdcall
#    endif
#    ifndef GLEWAPIENTRY
#      define GLEWAPIENTRY __stdcall
#    endif
#  else
#    define APIENTRY
#  endif
#endif
#ifndef GLAPI
#  if defined(__MINGW32__) || defined(__CYGWIN__)
#    define GLAPI extern
#  endif
#endif
/* <winnt.h> */
#ifndef CALLBACK
#define GLEW_CALLBACK_DEFINED
#  if defined(__MINGW32__) || defined(__CYGWIN__)
#    define CALLBACK __attribute__ ((__stdcall__))
#  elif (defined(_M_MRX000) || defined(_M_IX86) || defined(_M_ALPHA) || defined(_M_PPC)) && !defined(MIDL_PASS)
#    define CALLBACK __stdcall
#  else
#    define CALLBACK
#  endif
#endif
/* <wingdi.h> and <winnt.h> */
#ifndef WINGDIAPI
#define GLEW_WINGDIAPI_DEFINED
#define WINGDIAPI __declspec(dllimport)
#endif
/* <ctype.h> */
#if (defined(_MSC_VER) || defined(__BORLANDC__)) && !defined(_WCHAR_T_DEFINED)
typedef unsigned short wchar_t;
#  define _WCHAR_T_DEFINED
#endif
/* <stddef.h> */
#if !defined(_W64)
#  if !defined(__midl) && (defined(_X86_) || defined(_M_IX86)) && defined(_MSC_VER) && _MSC_VER >= 1300
#    define _W64 __w64
#  else
#    define _W64
#  endif
#endif
#if !defined(_PTRDIFF_T_DEFINED) && !defined(_PTRDIFF_T_) && !defined(__MINGW64__)
#  ifdef _WIN64
typedef __int64 ptrdiff_t;
#  else
typedef _W64 int ptrdiff_t;
#  endif
#  define _PTRDIFF_T_DEFINED
#  define _PTRDIFF_T_
#endif
#ifndef GLAPI
#  if defined(__MINGW32__) || defined(__CYGWIN__)
#    define GLAPI extern
#  else
#    define GLAPI WINGDIAPI
#  endif
#endif
/*
 * GLEW_STATIC is defined for static library.
 * GLEW_BUILD  is defined for building the DLL library.
 */
#ifdef GLEW_STATIC
#  define GLEWAPI extern
#else
#  ifdef GLEW_BUILD
#    define GLEWAPI extern __declspec(dllexport)
#  else
#    define GLEWAPI extern __declspec(dllimport)
#  endif
#endif
#else /* _UNIX */
/*
 * Needed for ptrdiff_t in turn needed by VBO.  This is defined by ISO
 * C.  On my system, this amounts to _3 lines_ of included code, all of
 * them pretty much harmless.  If you know of a way of detecting 32 vs
 * 64 _targets_ at compile time you are free to replace this with
 * something that's portable.  For now, _this_ is the portable solution.
 * (mem, 2004-01-04)
 */
#include <stddef.h>
/* SGI MIPSPro doesn't like stdint.h in C++ mode          */
/* ID: 3376260 Solaris 9 has inttypes.h, but not stdint.h */
#if (defined(__sgi) || defined(__sun)) && !defined(__GNUC__)
#include <inttypes.h>
#else
#include <stdint.h>
#endif
#define GLEW_APIENTRY_DEFINED
#define APIENTRY
/*
 * GLEW_STATIC is defined for static library.
 */
#ifdef GLEW_STATIC
#  define GLEWAPI extern
#else
#  if defined(__GNUC__) && __GNUC__>=4
#   define GLEWAPI extern __attribute__ ((visibility("default")))
#  elif defined(__SUNPRO_C) || defined(__SUNPRO_CC)
#   define GLEWAPI extern __global
#  else
#   define GLEWAPI extern
#  endif
#endif
/* <glu.h> */
#ifndef GLAPI
#define GLAPI extern
#endif
#endif /* _WIN32 */
#ifndef GLAPIENTRY
#define GLAPIENTRY
#endif
#ifndef GLEWAPIENTRY
#define GLEWAPIENTRY
#endif
#define GLEW_VAR_EXPORT GLEWAPI
#define GLEW_FUN_EXPORT GLEWAPI
#ifdef __cplusplus
extern "C" {
#endif
/* ----------------------------- GL_VERSION_1_1 ---------------------------- */
#ifndef GL_VERSION_1_1
typedef unsigned int GLenum;
typedef unsigned int GLbitfield;
typedef unsigned int GLuint;
typedef int GLint;
typedef int GLsizei;
typedef unsigned char GLboolean;
typedef signed char GLbyte;
typedef short GLshort;
typedef unsigned char GLubyte;
typedef unsigned short GLushort;
typedef unsigned long GLulong;
typedef float GLfloat;
typedef float GLclampf;
typedef double GLdouble;
typedef double GLclampd;
typedef void GLvoid;
#if defined(_MSC_VER) && _MSC_VER < 1400
typedef __int64 GLint64EXT;
typedef unsigned __int64 GLuint64EXT;
#elif defined(_MSC_VER) || defined(__BORLANDC__)
typedef signed long long GLint64EXT;
typedef unsigned long long GLuint64EXT;
#else
#  if defined(__MINGW32__) || defined(__CYGWIN__)
#include <inttypes.h>
#  endif
typedef int64_t GLint64EXT;
typedef uint64_t GLuint64EXT;
#endif
typedef GLint64EXT  GLint64;
typedef GLuint64EXT GLuint64;
typedef struct __GLsync *GLsync;
typedef char GLchar;
#endif /* GL_VERSION_1_1 */
/* ---------------------------------- GLU ---------------------------------- */
#ifndef GLEW_NO_GLU
#  ifdef __APPLE__
#    include <Availability.h>
#    if defined(__IPHONE_OS_VERSION_MIN_REQUIRED)
#      define GLEW_NO_GLU
#    endif
#  endif
#endif
#ifndef GLEW_NO_GLU
/* this is where we can safely include GLU */
#  if defined(__APPLE__) && defined(__MACH__)
#    include <OpenGL/glu.h>
#  else
#    include <GL/glu.h>
#  endif
#endif
/* ----------------------------- GL_VERSION_1_2 ---------------------------- */
#ifndef GL_VERSION_1_2
#endif /* GL_VERSION_1_2 */
/* ---------------------------- GL_VERSION_1_2_1 --------------------------- */
#ifndef GL_VERSION_1_2_1
#endif /* GL_VERSION_1_2_1 */
/* ----------------------------- GL_VERSION_1_3 ---------------------------- */
#ifndef GL_VERSION_1_3
#endif /* GL_VERSION_1_3 */
/* ----------------------------- GL_VERSION_1_4 ---------------------------- */
#ifndef GL_VERSION_1_4
#endif /* GL_VERSION_1_4 */
/* ----------------------------- GL_VERSION_1_5 ---------------------------- */
#ifndef GL_VERSION_1_5
typedef ptrdiff_t GLintptr;
typedef ptrdiff_t GLsizeiptr;
#endif /* GL_VERSION_1_5 */
/* ----------------------------- GL_VERSION_2_0 ---------------------------- */
#ifndef GL_VERSION_2_0
#endif /* GL_VERSION_2_0 */
/* ----------------------------- GL_VERSION_2_1 ---------------------------- */
#ifndef GL_VERSION_2_1
#endif /* GL_VERSION_2_1 */
/* ----------------------------- GL_VERSION_3_0 ---------------------------- */
#ifndef GL_VERSION_3_0
#endif /* GL_VERSION_3_0 */
/* ----------------------------- GL_VERSION_3_1 ---------------------------- */
#ifndef GL_VERSION_3_1
#endif /* GL_VERSION_3_1 */
/* ----------------------------- GL_VERSION_3_2 ---------------------------- */
#ifndef GL_VERSION_3_2
#endif /* GL_VERSION_3_2 */
/* ----------------------------- GL_VERSION_3_3 ---------------------------- */
#ifndef GL_VERSION_3_3
#endif /* GL_VERSION_3_3 */
/* ----------------------------- GL_VERSION_4_0 ---------------------------- */
#ifndef GL_VERSION_4_0
#endif /* GL_VERSION_4_0 */
/* ----------------------------- GL_VERSION_4_1 ---------------------------- */
#ifndef GL_VERSION_4_1
#endif /* GL_VERSION_4_1 */
/* ----------------------------- GL_VERSION_4_2 ---------------------------- */
#ifndef GL_VERSION_4_2
#endif /* GL_VERSION_4_2 */
/* ----------------------------- GL_VERSION_4_3 ---------------------------- */
#ifndef GL_VERSION_4_3
#endif /* GL_VERSION_4_3 */
/* ----------------------------- GL_VERSION_4_4 ---------------------------- */
#ifndef GL_VERSION_4_4
#endif /* GL_VERSION_4_4 */
/* ----------------------------- GL_VERSION_4_5 ---------------------------- */
#ifndef GL_VERSION_4_5
#endif /* GL_VERSION_4_5 */
/* ----------------------------- GL_VERSION_4_6 ---------------------------- */
#ifndef GL_VERSION_4_6
#endif /* GL_VERSION_4_6 */
/* -------------------------- GL_3DFX_multisample -------------------------- */
#ifndef GL_3DFX_multisample
#endif /* GL_3DFX_multisample */
/* ---------------------------- GL_3DFX_tbuffer ---------------------------- */
#ifndef GL_3DFX_tbuffer
#endif /* GL_3DFX_tbuffer */
/* -------------------- GL_3DFX_texture_compression_FXT1 ------------------- */
#ifndef GL_3DFX_texture_compression_FXT1
#endif /* GL_3DFX_texture_compression_FXT1 */
/* ----------------------- GL_AMD_blend_minmax_factor ---------------------- */
#ifndef GL_AMD_blend_minmax_factor
#endif /* GL_AMD_blend_minmax_factor */
/* --------------------- GL_AMD_compressed_3DC_texture --------------------- */
#ifndef GL_AMD_compressed_3DC_texture
#endif /* GL_AMD_compressed_3DC_texture */
/* --------------------- GL_AMD_compressed_ATC_texture --------------------- */
#ifndef GL_AMD_compressed_ATC_texture
#endif /* GL_AMD_compressed_ATC_texture */
/* ----------------------- GL_AMD_conservative_depth ----------------------- */
#ifndef GL_AMD_conservative_depth
#endif /* GL_AMD_conservative_depth */
/* -------------------------- GL_AMD_debug_output -------------------------- */
#ifndef GL_AMD_debug_output
#endif /* GL_AMD_debug_output */
/* ---------------------- GL_AMD_depth_clamp_separate ---------------------- */
#ifndef GL_AMD_depth_clamp_separate
#endif /* GL_AMD_depth_clamp_separate */
/* ----------------------- GL_AMD_draw_buffers_blend ----------------------- */
#ifndef GL_AMD_draw_buffers_blend
#endif /* GL_AMD_draw_buffers_blend */
/* ------------------ GL_AMD_framebuffer_sample_positions ------------------ */
#ifndef GL_AMD_framebuffer_sample_positions
#endif /* GL_AMD_framebuffer_sample_positions */
/* --------------------------- GL_AMD_gcn_shader --------------------------- */
#ifndef GL_AMD_gcn_shader
#endif /* GL_AMD_gcn_shader */
/* ---------------------- GL_AMD_gpu_shader_half_float --------------------- */
#ifndef GL_AMD_gpu_shader_half_float
#endif /* GL_AMD_gpu_shader_half_float */
/* ------------------------ GL_AMD_gpu_shader_int16 ------------------------ */
#ifndef GL_AMD_gpu_shader_int16
#endif /* GL_AMD_gpu_shader_int16 */
/* ------------------------ GL_AMD_gpu_shader_int64 ------------------------ */
#ifndef GL_AMD_gpu_shader_int64
#endif /* GL_AMD_gpu_shader_int64 */
/* ---------------------- GL_AMD_interleaved_elements ---------------------- */
#ifndef GL_AMD_interleaved_elements
#endif /* GL_AMD_interleaved_elements */
/* ----------------------- GL_AMD_multi_draw_indirect ---------------------- */
#ifndef GL_AMD_multi_draw_indirect
#endif /* GL_AMD_multi_draw_indirect */
/* ------------------------- GL_AMD_name_gen_delete ------------------------ */
#ifndef GL_AMD_name_gen_delete
#endif /* GL_AMD_name_gen_delete */
/* ---------------------- GL_AMD_occlusion_query_event --------------------- */
#ifndef GL_AMD_occlusion_query_event
#endif /* GL_AMD_occlusion_query_event */
/* ----------------------- GL_AMD_performance_monitor ---------------------- */
#ifndef GL_AMD_performance_monitor
#endif /* GL_AMD_performance_monitor */
/* -------------------------- GL_AMD_pinned_memory ------------------------- */
#ifndef GL_AMD_pinned_memory
#endif /* GL_AMD_pinned_memory */
/* ----------------------- GL_AMD_program_binary_Z400 ---------------------- */
#ifndef GL_AMD_program_binary_Z400
#endif /* GL_AMD_program_binary_Z400 */
/* ----------------------- GL_AMD_query_buffer_object ---------------------- */
#ifndef GL_AMD_query_buffer_object
#endif /* GL_AMD_query_buffer_object */
/* ------------------------ GL_AMD_sample_positions ------------------------ */
#ifndef GL_AMD_sample_positions
#endif /* GL_AMD_sample_positions */
/* ------------------ GL_AMD_seamless_cubemap_per_texture ------------------ */
#ifndef GL_AMD_seamless_cubemap_per_texture
#endif /* GL_AMD_seamless_cubemap_per_texture */
/* -------------------- GL_AMD_shader_atomic_counter_ops ------------------- */
#ifndef GL_AMD_shader_atomic_counter_ops
#endif /* GL_AMD_shader_atomic_counter_ops */
/* -------------------------- GL_AMD_shader_ballot ------------------------- */
#ifndef GL_AMD_shader_ballot
#endif /* GL_AMD_shader_ballot */
/* ---------------- GL_AMD_shader_explicit_vertex_parameter ---------------- */
#ifndef GL_AMD_shader_explicit_vertex_parameter
#endif /* GL_AMD_shader_explicit_vertex_parameter */
/* ---------------------- GL_AMD_shader_stencil_export --------------------- */
#ifndef GL_AMD_shader_stencil_export
#endif /* GL_AMD_shader_stencil_export */
/* ------------------- GL_AMD_shader_stencil_value_export ------------------ */
#ifndef GL_AMD_shader_stencil_value_export
#endif /* GL_AMD_shader_stencil_value_export */
/* ---------------------- GL_AMD_shader_trinary_minmax --------------------- */
#ifndef GL_AMD_shader_trinary_minmax
#endif /* GL_AMD_shader_trinary_minmax */
/* ------------------------- GL_AMD_sparse_texture ------------------------- */
#ifndef GL_AMD_sparse_texture
#endif /* GL_AMD_sparse_texture */
/* ------------------- GL_AMD_stencil_operation_extended ------------------- */
#ifndef GL_AMD_stencil_operation_extended
#endif /* GL_AMD_stencil_operation_extended */
/* --------------------- GL_AMD_texture_gather_bias_lod -------------------- */
#ifndef GL_AMD_texture_gather_bias_lod
#endif /* GL_AMD_texture_gather_bias_lod */
/* ------------------------ GL_AMD_texture_texture4 ------------------------ */
#ifndef GL_AMD_texture_texture4
#endif /* GL_AMD_texture_texture4 */
/* --------------- GL_AMD_transform_feedback3_lines_triangles -------------- */
#ifndef GL_AMD_transform_feedback3_lines_triangles
#endif /* GL_AMD_transform_feedback3_lines_triangles */
/* ----------------------- GL_AMD_transform_feedback4 ---------------------- */
#ifndef GL_AMD_transform_feedback4
#endif /* GL_AMD_transform_feedback4 */
/* ----------------------- GL_AMD_vertex_shader_layer ---------------------- */
#ifndef GL_AMD_vertex_shader_layer
#endif /* GL_AMD_vertex_shader_layer */
/* -------------------- GL_AMD_vertex_shader_tessellator ------------------- */
#ifndef GL_AMD_vertex_shader_tessellator
#endif /* GL_AMD_vertex_shader_tessellator */
/* ------------------ GL_AMD_vertex_shader_viewport_index ------------------ */
#ifndef GL_AMD_vertex_shader_viewport_index
#endif /* GL_AMD_vertex_shader_viewport_index */
/* -------------------- GL_ANDROID_extension_pack_es31a -------------------- */
#ifndef GL_ANDROID_extension_pack_es31a
#endif /* GL_ANDROID_extension_pack_es31a */
/* ------------------------- GL_ANGLE_depth_texture ------------------------ */
#ifndef GL_ANGLE_depth_texture
#endif /* GL_ANGLE_depth_texture */
/* ----------------------- GL_ANGLE_framebuffer_blit ----------------------- */
#ifndef GL_ANGLE_framebuffer_blit
#endif /* GL_ANGLE_framebuffer_blit */
/* -------------------- GL_ANGLE_framebuffer_multisample ------------------- */
#ifndef GL_ANGLE_framebuffer_multisample
#endif /* GL_ANGLE_framebuffer_multisample */
/* ----------------------- GL_ANGLE_instanced_arrays ----------------------- */
#ifndef GL_ANGLE_instanced_arrays
#endif /* GL_ANGLE_instanced_arrays */
/* -------------------- GL_ANGLE_pack_reverse_row_order -------------------- */
#ifndef GL_ANGLE_pack_reverse_row_order
#endif /* GL_ANGLE_pack_reverse_row_order */
/* ------------------------ GL_ANGLE_program_binary ------------------------ */
#ifndef GL_ANGLE_program_binary
#endif /* GL_ANGLE_program_binary */
/* ------------------- GL_ANGLE_texture_compression_dxt1 ------------------- */
#ifndef GL_ANGLE_texture_compression_dxt1
#endif /* GL_ANGLE_texture_compression_dxt1 */
/* ------------------- GL_ANGLE_texture_compression_dxt3 ------------------- */
#ifndef GL_ANGLE_texture_compression_dxt3
#endif /* GL_ANGLE_texture_compression_dxt3 */
/* ------------------- GL_ANGLE_texture_compression_dxt5 ------------------- */
#ifndef GL_ANGLE_texture_compression_dxt5
#endif /* GL_ANGLE_texture_compression_dxt5 */
/* ------------------------- GL_ANGLE_texture_usage ------------------------ */
#ifndef GL_ANGLE_texture_usage
#endif /* GL_ANGLE_texture_usage */
/* -------------------------- GL_ANGLE_timer_query ------------------------- */
#ifndef GL_ANGLE_timer_query
#endif /* GL_ANGLE_timer_query */
/* ------------------- GL_ANGLE_translated_shader_source ------------------- */
#ifndef GL_ANGLE_translated_shader_source
#endif /* GL_ANGLE_translated_shader_source */
/* ----------------------- GL_APPLE_aux_depth_stencil ---------------------- */
#ifndef GL_APPLE_aux_depth_stencil
#endif /* GL_APPLE_aux_depth_stencil */
/* ------------------------ GL_APPLE_client_storage ------------------------ */
#ifndef GL_APPLE_client_storage
#endif /* GL_APPLE_client_storage */
/* ------------------------- GL_APPLE_clip_distance ------------------------ */
#ifndef GL_APPLE_clip_distance
#endif /* GL_APPLE_clip_distance */
/* ------------------- GL_APPLE_color_buffer_packed_float ------------------ */
#ifndef GL_APPLE_color_buffer_packed_float
#endif /* GL_APPLE_color_buffer_packed_float */
/* ---------------------- GL_APPLE_copy_texture_levels --------------------- */
#ifndef GL_APPLE_copy_texture_levels
#endif /* GL_APPLE_copy_texture_levels */
/* ------------------------- GL_APPLE_element_array ------------------------ */
#ifndef GL_APPLE_element_array
#endif /* GL_APPLE_element_array */
/* ----------------------------- GL_APPLE_fence ---------------------------- */
#ifndef GL_APPLE_fence
#endif /* GL_APPLE_fence */
/* ------------------------- GL_APPLE_float_pixels ------------------------- */
#ifndef GL_APPLE_float_pixels
#endif /* GL_APPLE_float_pixels */
/* ---------------------- GL_APPLE_flush_buffer_range ---------------------- */
#ifndef GL_APPLE_flush_buffer_range
#endif /* GL_APPLE_flush_buffer_range */
/* -------------------- GL_APPLE_framebuffer_multisample ------------------- */
#ifndef GL_APPLE_framebuffer_multisample
#endif /* GL_APPLE_framebuffer_multisample */
/* ----------------------- GL_APPLE_object_purgeable ----------------------- */
#ifndef GL_APPLE_object_purgeable
#endif /* GL_APPLE_object_purgeable */
/* ------------------------- GL_APPLE_pixel_buffer ------------------------- */
#ifndef GL_APPLE_pixel_buffer
#endif /* GL_APPLE_pixel_buffer */
/* ---------------------------- GL_APPLE_rgb_422 --------------------------- */
#ifndef GL_APPLE_rgb_422
#endif /* GL_APPLE_rgb_422 */
/* --------------------------- GL_APPLE_row_bytes -------------------------- */
#ifndef GL_APPLE_row_bytes
#endif /* GL_APPLE_row_bytes */
/* ------------------------ GL_APPLE_specular_vector ----------------------- */
#ifndef GL_APPLE_specular_vector
#endif /* GL_APPLE_specular_vector */
/* ----------------------------- GL_APPLE_sync ----------------------------- */
#ifndef GL_APPLE_sync
#endif /* GL_APPLE_sync */
/* -------------------- GL_APPLE_texture_2D_limited_npot ------------------- */
#ifndef GL_APPLE_texture_2D_limited_npot
#endif /* GL_APPLE_texture_2D_limited_npot */
/* -------------------- GL_APPLE_texture_format_BGRA8888 ------------------- */
#ifndef GL_APPLE_texture_format_BGRA8888
#endif /* GL_APPLE_texture_format_BGRA8888 */
/* ----------------------- GL_APPLE_texture_max_level ---------------------- */
#ifndef GL_APPLE_texture_max_level
#endif /* GL_APPLE_texture_max_level */
/* --------------------- GL_APPLE_texture_packed_float --------------------- */
#ifndef GL_APPLE_texture_packed_float
#endif /* GL_APPLE_texture_packed_float */
/* ------------------------- GL_APPLE_texture_range ------------------------ */
#ifndef GL_APPLE_texture_range
#endif /* GL_APPLE_texture_range */
/* ------------------------ GL_APPLE_transform_hint ------------------------ */
#ifndef GL_APPLE_transform_hint
#endif /* GL_APPLE_transform_hint */
/* ---------------------- GL_APPLE_vertex_array_object --------------------- */
#ifndef GL_APPLE_vertex_array_object
#endif /* GL_APPLE_vertex_array_object */
/* ---------------------- GL_APPLE_vertex_array_range ---------------------- */
#ifndef GL_APPLE_vertex_array_range
#endif /* GL_APPLE_vertex_array_range */
/* ------------------- GL_APPLE_vertex_program_evaluators ------------------ */
#ifndef GL_APPLE_vertex_program_evaluators
#endif /* GL_APPLE_vertex_program_evaluators */
/* --------------------------- GL_APPLE_ycbcr_422 -------------------------- */
#ifndef GL_APPLE_ycbcr_422
#endif /* GL_APPLE_ycbcr_422 */
/* ------------------------ GL_ARB_ES2_compatibility ----------------------- */
#ifndef GL_ARB_ES2_compatibility
typedef int GLfixed;
#endif /* GL_ARB_ES2_compatibility */
/* ----------------------- GL_ARB_ES3_1_compatibility ---------------------- */
#ifndef GL_ARB_ES3_1_compatibility
#endif /* GL_ARB_ES3_1_compatibility */
/* ----------------------- GL_ARB_ES3_2_compatibility ---------------------- */
#ifndef GL_ARB_ES3_2_compatibility
#endif /* GL_ARB_ES3_2_compatibility */
/* ------------------------ GL_ARB_ES3_compatibility ----------------------- */
#ifndef GL_ARB_ES3_compatibility
#endif /* GL_ARB_ES3_compatibility */
/* ------------------------ GL_ARB_arrays_of_arrays ------------------------ */
#ifndef GL_ARB_arrays_of_arrays
#endif /* GL_ARB_arrays_of_arrays */
/* -------------------------- GL_ARB_base_instance ------------------------- */
#ifndef GL_ARB_base_instance
#endif /* GL_ARB_base_instance */
/* ------------------------ GL_ARB_bindless_texture ------------------------ */
#ifndef GL_ARB_bindless_texture
#endif /* GL_ARB_bindless_texture */
/* ----------------------- GL_ARB_blend_func_extended ---------------------- */
#ifndef GL_ARB_blend_func_extended
#endif /* GL_ARB_blend_func_extended */
/* ------------------------- GL_ARB_buffer_storage ------------------------- */
#ifndef GL_ARB_buffer_storage
#endif /* GL_ARB_buffer_storage */
/* ---------------------------- GL_ARB_cl_event ---------------------------- */
#ifndef GL_ARB_cl_event
typedef struct _cl_context *cl_context;
typedef struct _cl_event *cl_event;
#endif /* GL_ARB_cl_event */
/* ----------------------- GL_ARB_clear_buffer_object ---------------------- */
#ifndef GL_ARB_clear_buffer_object
#endif /* GL_ARB_clear_buffer_object */
/* -------------------------- GL_ARB_clear_texture ------------------------- */
#ifndef GL_ARB_clear_texture
#endif /* GL_ARB_clear_texture */
/* -------------------------- GL_ARB_clip_control -------------------------- */
#ifndef GL_ARB_clip_control
#endif /* GL_ARB_clip_control */
/* ----------------------- GL_ARB_color_buffer_float ----------------------- */
#ifndef GL_ARB_color_buffer_float
#endif /* GL_ARB_color_buffer_float */
/* -------------------------- GL_ARB_compatibility ------------------------- */
#ifndef GL_ARB_compatibility
#endif /* GL_ARB_compatibility */
/* ---------------- GL_ARB_compressed_texture_pixel_storage ---------------- */
#ifndef GL_ARB_compressed_texture_pixel_storage
#endif /* GL_ARB_compressed_texture_pixel_storage */
/* ------------------------- GL_ARB_compute_shader ------------------------- */
#ifndef GL_ARB_compute_shader
#endif /* GL_ARB_compute_shader */
/* ------------------- GL_ARB_compute_variable_group_size ------------------ */
#ifndef GL_ARB_compute_variable_group_size
#endif /* GL_ARB_compute_variable_group_size */
/* ------------------- GL_ARB_conditional_render_inverted ------------------ */
#ifndef GL_ARB_conditional_render_inverted
#endif /* GL_ARB_conditional_render_inverted */
/* ----------------------- GL_ARB_conservative_depth ----------------------- */
#ifndef GL_ARB_conservative_depth
#endif /* GL_ARB_conservative_depth */
/* --------------------------- GL_ARB_copy_buffer -------------------------- */
#ifndef GL_ARB_copy_buffer
#endif /* GL_ARB_copy_buffer */
/* --------------------------- GL_ARB_copy_image --------------------------- */
#ifndef GL_ARB_copy_image
#endif /* GL_ARB_copy_image */
/* -------------------------- GL_ARB_cull_distance ------------------------- */
#ifndef GL_ARB_cull_distance
#endif /* GL_ARB_cull_distance */
/* -------------------------- GL_ARB_debug_output -------------------------- */
#ifndef GL_ARB_debug_output
#endif /* GL_ARB_debug_output */
/* ----------------------- GL_ARB_depth_buffer_float ----------------------- */
#ifndef GL_ARB_depth_buffer_float
#endif /* GL_ARB_depth_buffer_float */
/* --------------------------- GL_ARB_depth_clamp -------------------------- */
#ifndef GL_ARB_depth_clamp
#endif /* GL_ARB_depth_clamp */
/* -------------------------- GL_ARB_depth_texture ------------------------- */
#ifndef GL_ARB_depth_texture
#endif /* GL_ARB_depth_texture */
/* ----------------------- GL_ARB_derivative_control ----------------------- */
#ifndef GL_ARB_derivative_control
#endif /* GL_ARB_derivative_control */
/* ----------------------- GL_ARB_direct_state_access ---------------------- */
#ifndef GL_ARB_direct_state_access
#endif /* GL_ARB_direct_state_access */
/* -------------------------- GL_ARB_draw_buffers -------------------------- */
#ifndef GL_ARB_draw_buffers
#endif /* GL_ARB_draw_buffers */
/* ----------------------- GL_ARB_draw_buffers_blend ----------------------- */
#ifndef GL_ARB_draw_buffers_blend
#endif /* GL_ARB_draw_buffers_blend */
/* -------------------- GL_ARB_draw_elements_base_vertex ------------------- */
#ifndef GL_ARB_draw_elements_base_vertex
#endif /* GL_ARB_draw_elements_base_vertex */
/* -------------------------- GL_ARB_draw_indirect ------------------------- */
#ifndef GL_ARB_draw_indirect
#endif /* GL_ARB_draw_indirect */
/* ------------------------- GL_ARB_draw_instanced ------------------------- */
#ifndef GL_ARB_draw_instanced
#endif /* GL_ARB_draw_instanced */
/* ------------------------ GL_ARB_enhanced_layouts ------------------------ */
#ifndef GL_ARB_enhanced_layouts
#endif /* GL_ARB_enhanced_layouts */
/* -------------------- GL_ARB_explicit_attrib_location -------------------- */
#ifndef GL_ARB_explicit_attrib_location
#endif /* GL_ARB_explicit_attrib_location */
/* -------------------- GL_ARB_explicit_uniform_location ------------------- */
#ifndef GL_ARB_explicit_uniform_location
#endif /* GL_ARB_explicit_uniform_location */
/* ------------------- GL_ARB_fragment_coord_conventions ------------------- */
#ifndef GL_ARB_fragment_coord_conventions
#endif /* GL_ARB_fragment_coord_conventions */
/* --------------------- GL_ARB_fragment_layer_viewport -------------------- */
#ifndef GL_ARB_fragment_layer_viewport
#endif /* GL_ARB_fragment_layer_viewport */
/* ------------------------ GL_ARB_fragment_program ------------------------ */
#ifndef GL_ARB_fragment_program
#endif /* GL_ARB_fragment_program */
/* --------------------- GL_ARB_fragment_program_shadow -------------------- */
#ifndef GL_ARB_fragment_program_shadow
#endif /* GL_ARB_fragment_program_shadow */
/* ------------------------- GL_ARB_fragment_shader ------------------------ */
#ifndef GL_ARB_fragment_shader
#endif /* GL_ARB_fragment_shader */
/* -------------------- GL_ARB_fragment_shader_interlock ------------------- */
#ifndef GL_ARB_fragment_shader_interlock
#endif /* GL_ARB_fragment_shader_interlock */
/* ------------------- GL_ARB_framebuffer_no_attachments ------------------- */
#ifndef GL_ARB_framebuffer_no_attachments
#endif /* GL_ARB_framebuffer_no_attachments */
/* ----------------------- GL_ARB_framebuffer_object ----------------------- */
#ifndef GL_ARB_framebuffer_object
#endif /* GL_ARB_framebuffer_object */
/* ------------------------ GL_ARB_framebuffer_sRGB ------------------------ */
#ifndef GL_ARB_framebuffer_sRGB
#endif /* GL_ARB_framebuffer_sRGB */
/* ------------------------ GL_ARB_geometry_shader4 ------------------------ */
#ifndef GL_ARB_geometry_shader4
#endif /* GL_ARB_geometry_shader4 */
/* ----------------------- GL_ARB_get_program_binary ----------------------- */
#ifndef GL_ARB_get_program_binary
#endif /* GL_ARB_get_program_binary */
/* ---------------------- GL_ARB_get_texture_sub_image --------------------- */
#ifndef GL_ARB_get_texture_sub_image
#endif /* GL_ARB_get_texture_sub_image */
/* ---------------------------- GL_ARB_gl_spirv ---------------------------- */
#ifndef GL_ARB_gl_spirv
#endif /* GL_ARB_gl_spirv */
/* --------------------------- GL_ARB_gpu_shader5 -------------------------- */
#ifndef GL_ARB_gpu_shader5
#endif /* GL_ARB_gpu_shader5 */
/* ------------------------- GL_ARB_gpu_shader_fp64 ------------------------ */
#ifndef GL_ARB_gpu_shader_fp64
#endif /* GL_ARB_gpu_shader_fp64 */
/* ------------------------ GL_ARB_gpu_shader_int64 ------------------------ */
#ifndef GL_ARB_gpu_shader_int64
#endif /* GL_ARB_gpu_shader_int64 */
/* ------------------------ GL_ARB_half_float_pixel ------------------------ */
#ifndef GL_ARB_half_float_pixel
#endif /* GL_ARB_half_float_pixel */
/* ------------------------ GL_ARB_half_float_vertex ----------------------- */
#ifndef GL_ARB_half_float_vertex
#endif /* GL_ARB_half_float_vertex */
/* ----------------------------- GL_ARB_imaging ---------------------------- */
#ifndef GL_ARB_imaging
#endif /* GL_ARB_imaging */
/* ----------------------- GL_ARB_indirect_parameters ---------------------- */
#ifndef GL_ARB_indirect_parameters
#endif /* GL_ARB_indirect_parameters */
/* ------------------------ GL_ARB_instanced_arrays ------------------------ */
#ifndef GL_ARB_instanced_arrays
#endif /* GL_ARB_instanced_arrays */
/* ---------------------- GL_ARB_internalformat_query ---------------------- */
#ifndef GL_ARB_internalformat_query
#endif /* GL_ARB_internalformat_query */
/* ---------------------- GL_ARB_internalformat_query2 --------------------- */
#ifndef GL_ARB_internalformat_query2
#endif /* GL_ARB_internalformat_query2 */
/* ----------------------- GL_ARB_invalidate_subdata ----------------------- */
#ifndef GL_ARB_invalidate_subdata
#endif /* GL_ARB_invalidate_subdata */
/* ---------------------- GL_ARB_map_buffer_alignment ---------------------- */
#ifndef GL_ARB_map_buffer_alignment
#endif /* GL_ARB_map_buffer_alignment */
/* ------------------------ GL_ARB_map_buffer_range ------------------------ */
#ifndef GL_ARB_map_buffer_range
#endif /* GL_ARB_map_buffer_range */
/* ------------------------- GL_ARB_matrix_palette ------------------------- */
#ifndef GL_ARB_matrix_palette
#endif /* GL_ARB_matrix_palette */
/* --------------------------- GL_ARB_multi_bind --------------------------- */
#ifndef GL_ARB_multi_bind
#endif /* GL_ARB_multi_bind */
/* ----------------------- GL_ARB_multi_draw_indirect ---------------------- */
#ifndef GL_ARB_multi_draw_indirect
#endif /* GL_ARB_multi_draw_indirect */
/* --------------------------- GL_ARB_multisample -------------------------- */
#ifndef GL_ARB_multisample
#endif /* GL_ARB_multisample */
/* -------------------------- GL_ARB_multitexture -------------------------- */
#ifndef GL_ARB_multitexture
#endif /* GL_ARB_multitexture */
/* ------------------------- GL_ARB_occlusion_query ------------------------ */
#ifndef GL_ARB_occlusion_query
#endif /* GL_ARB_occlusion_query */
/* ------------------------ GL_ARB_occlusion_query2 ------------------------ */
#ifndef GL_ARB_occlusion_query2
#endif /* GL_ARB_occlusion_query2 */
/* --------------------- GL_ARB_parallel_shader_compile -------------------- */
#ifndef GL_ARB_parallel_shader_compile
#endif /* GL_ARB_parallel_shader_compile */
/* -------------------- GL_ARB_pipeline_statistics_query ------------------- */
#ifndef GL_ARB_pipeline_statistics_query
#endif /* GL_ARB_pipeline_statistics_query */
/* ----------------------- GL_ARB_pixel_buffer_object ---------------------- */
#ifndef GL_ARB_pixel_buffer_object
#endif /* GL_ARB_pixel_buffer_object */
/* ------------------------ GL_ARB_point_parameters ------------------------ */
#ifndef GL_ARB_point_parameters
#endif /* GL_ARB_point_parameters */
/* -------------------------- GL_ARB_point_sprite -------------------------- */
#ifndef GL_ARB_point_sprite
#endif /* GL_ARB_point_sprite */
/* ---------------------- GL_ARB_polygon_offset_clamp ---------------------- */
#ifndef GL_ARB_polygon_offset_clamp
#endif /* GL_ARB_polygon_offset_clamp */
/* ----------------------- GL_ARB_post_depth_coverage ---------------------- */
#ifndef GL_ARB_post_depth_coverage
#endif /* GL_ARB_post_depth_coverage */
/* --------------------- GL_ARB_program_interface_query -------------------- */
#ifndef GL_ARB_program_interface_query
#endif /* GL_ARB_program_interface_query */
/* ------------------------ GL_ARB_provoking_vertex ------------------------ */
#ifndef GL_ARB_provoking_vertex
#endif /* GL_ARB_provoking_vertex */
/* ----------------------- GL_ARB_query_buffer_object ---------------------- */
#ifndef GL_ARB_query_buffer_object
#endif /* GL_ARB_query_buffer_object */
/* ------------------ GL_ARB_robust_buffer_access_behavior ----------------- */
#ifndef GL_ARB_robust_buffer_access_behavior
#endif /* GL_ARB_robust_buffer_access_behavior */
/* --------------------------- GL_ARB_robustness --------------------------- */
#ifndef GL_ARB_robustness
#endif /* GL_ARB_robustness */
/* ---------------- GL_ARB_robustness_application_isolation ---------------- */
#ifndef GL_ARB_robustness_application_isolation
#endif /* GL_ARB_robustness_application_isolation */
/* ---------------- GL_ARB_robustness_share_group_isolation ---------------- */
#ifndef GL_ARB_robustness_share_group_isolation
#endif /* GL_ARB_robustness_share_group_isolation */
/* ------------------------ GL_ARB_sample_locations ------------------------ */
#ifndef GL_ARB_sample_locations
#endif /* GL_ARB_sample_locations */
/* ------------------------- GL_ARB_sample_shading ------------------------- */
#ifndef GL_ARB_sample_shading
#endif /* GL_ARB_sample_shading */
/* ------------------------- GL_ARB_sampler_objects ------------------------ */
#ifndef GL_ARB_sampler_objects
#endif /* GL_ARB_sampler_objects */
/* ------------------------ GL_ARB_seamless_cube_map ----------------------- */
#ifndef GL_ARB_seamless_cube_map
#endif /* GL_ARB_seamless_cube_map */
/* ------------------ GL_ARB_seamless_cubemap_per_texture ------------------ */
#ifndef GL_ARB_seamless_cubemap_per_texture
#endif /* GL_ARB_seamless_cubemap_per_texture */
/* --------------------- GL_ARB_separate_shader_objects -------------------- */
#ifndef GL_ARB_separate_shader_objects
#endif /* GL_ARB_separate_shader_objects */
/* -------------------- GL_ARB_shader_atomic_counter_ops ------------------- */
#ifndef GL_ARB_shader_atomic_counter_ops
#endif /* GL_ARB_shader_atomic_counter_ops */
/* --------------------- GL_ARB_shader_atomic_counters --------------------- */
#ifndef GL_ARB_shader_atomic_counters
#endif /* GL_ARB_shader_atomic_counters */
/* -------------------------- GL_ARB_shader_ballot ------------------------- */
#ifndef GL_ARB_shader_ballot
#endif /* GL_ARB_shader_ballot */
/* ----------------------- GL_ARB_shader_bit_encoding ---------------------- */
#ifndef GL_ARB_shader_bit_encoding
#endif /* GL_ARB_shader_bit_encoding */
/* -------------------------- GL_ARB_shader_clock -------------------------- */
#ifndef GL_ARB_shader_clock
#endif /* GL_ARB_shader_clock */
/* --------------------- GL_ARB_shader_draw_parameters --------------------- */
#ifndef GL_ARB_shader_draw_parameters
#endif /* GL_ARB_shader_draw_parameters */
/* ------------------------ GL_ARB_shader_group_vote ----------------------- */
#ifndef GL_ARB_shader_group_vote
#endif /* GL_ARB_shader_group_vote */
/* --------------------- GL_ARB_shader_image_load_store -------------------- */
#ifndef GL_ARB_shader_image_load_store
#endif /* GL_ARB_shader_image_load_store */
/* ------------------------ GL_ARB_shader_image_size ----------------------- */
#ifndef GL_ARB_shader_image_size
#endif /* GL_ARB_shader_image_size */
/* ------------------------- GL_ARB_shader_objects ------------------------- */
#ifndef GL_ARB_shader_objects
typedef char GLcharARB;
typedef unsigned int GLhandleARB;
#endif /* GL_ARB_shader_objects */
/* ------------------------ GL_ARB_shader_precision ------------------------ */
#ifndef GL_ARB_shader_precision
#endif /* GL_ARB_shader_precision */
/* ---------------------- GL_ARB_shader_stencil_export --------------------- */
#ifndef GL_ARB_shader_stencil_export
#endif /* GL_ARB_shader_stencil_export */
/* ------------------ GL_ARB_shader_storage_buffer_object ------------------ */
#ifndef GL_ARB_shader_storage_buffer_object
#endif /* GL_ARB_shader_storage_buffer_object */
/* ------------------------ GL_ARB_shader_subroutine ----------------------- */
#ifndef GL_ARB_shader_subroutine
#endif /* GL_ARB_shader_subroutine */
/* ------------------ GL_ARB_shader_texture_image_samples ------------------ */
#ifndef GL_ARB_shader_texture_image_samples
#endif /* GL_ARB_shader_texture_image_samples */
/* ----------------------- GL_ARB_shader_texture_lod ----------------------- */
#ifndef GL_ARB_shader_texture_lod
#endif /* GL_ARB_shader_texture_lod */
/* ------------------- GL_ARB_shader_viewport_layer_array ------------------ */
#ifndef GL_ARB_shader_viewport_layer_array
#endif /* GL_ARB_shader_viewport_layer_array */
/* ---------------------- GL_ARB_shading_language_100 ---------------------- */
#ifndef GL_ARB_shading_language_100
#endif /* GL_ARB_shading_language_100 */
/* -------------------- GL_ARB_shading_language_420pack -------------------- */
#ifndef GL_ARB_shading_language_420pack
#endif /* GL_ARB_shading_language_420pack */
/* -------------------- GL_ARB_shading_language_include -------------------- */
#ifndef GL_ARB_shading_language_include
#endif /* GL_ARB_shading_language_include */
/* -------------------- GL_ARB_shading_language_packing -------------------- */
#ifndef GL_ARB_shading_language_packing
#endif /* GL_ARB_shading_language_packing */
/* ----------------------------- GL_ARB_shadow ----------------------------- */
#ifndef GL_ARB_shadow
#endif /* GL_ARB_shadow */
/* ------------------------- GL_ARB_shadow_ambient ------------------------- */
#ifndef GL_ARB_shadow_ambient
#endif /* GL_ARB_shadow_ambient */
/* -------------------------- GL_ARB_sparse_buffer ------------------------- */
#ifndef GL_ARB_sparse_buffer
#endif /* GL_ARB_sparse_buffer */
/* ------------------------- GL_ARB_sparse_texture ------------------------- */
#ifndef GL_ARB_sparse_texture
#endif /* GL_ARB_sparse_texture */
/* ------------------------- GL_ARB_sparse_texture2 ------------------------ */
#ifndef GL_ARB_sparse_texture2
#endif /* GL_ARB_sparse_texture2 */
/* ---------------------- GL_ARB_sparse_texture_clamp ---------------------- */
#ifndef GL_ARB_sparse_texture_clamp
#endif /* GL_ARB_sparse_texture_clamp */
/* ------------------------ GL_ARB_spirv_extensions ------------------------ */
#ifndef GL_ARB_spirv_extensions
#endif /* GL_ARB_spirv_extensions */
/* ------------------------ GL_ARB_stencil_texturing ----------------------- */
#ifndef GL_ARB_stencil_texturing
#endif /* GL_ARB_stencil_texturing */
/* ------------------------------ GL_ARB_sync ------------------------------ */
#ifndef GL_ARB_sync
#endif /* GL_ARB_sync */
/* ----------------------- GL_ARB_tessellation_shader ---------------------- */
#ifndef GL_ARB_tessellation_shader
#endif /* GL_ARB_tessellation_shader */
/* ------------------------- GL_ARB_texture_barrier ------------------------ */
#ifndef GL_ARB_texture_barrier
#endif /* GL_ARB_texture_barrier */
/* ---------------------- GL_ARB_texture_border_clamp ---------------------- */
#ifndef GL_ARB_texture_border_clamp
#endif /* GL_ARB_texture_border_clamp */
/* ---------------------- GL_ARB_texture_buffer_object --------------------- */
#ifndef GL_ARB_texture_buffer_object
#endif /* GL_ARB_texture_buffer_object */
/* ------------------- GL_ARB_texture_buffer_object_rgb32 ------------------ */
#ifndef GL_ARB_texture_buffer_object_rgb32
#endif /* GL_ARB_texture_buffer_object_rgb32 */
/* ---------------------- GL_ARB_texture_buffer_range ---------------------- */
#ifndef GL_ARB_texture_buffer_range
#endif /* GL_ARB_texture_buffer_range */
/* ----------------------- GL_ARB_texture_compression ---------------------- */
#ifndef GL_ARB_texture_compression
#endif /* GL_ARB_texture_compression */
/* -------------------- GL_ARB_texture_compression_bptc -------------------- */
#ifndef GL_ARB_texture_compression_bptc
#endif /* GL_ARB_texture_compression_bptc */
/* -------------------- GL_ARB_texture_compression_rgtc -------------------- */
#ifndef GL_ARB_texture_compression_rgtc
#endif /* GL_ARB_texture_compression_rgtc */
/* ------------------------ GL_ARB_texture_cube_map ------------------------ */
#ifndef GL_ARB_texture_cube_map
#endif /* GL_ARB_texture_cube_map */
/* --------------------- GL_ARB_texture_cube_map_array --------------------- */
#ifndef GL_ARB_texture_cube_map_array
#endif /* GL_ARB_texture_cube_map_array */
/* ------------------------- GL_ARB_texture_env_add ------------------------ */
#ifndef GL_ARB_texture_env_add
#endif /* GL_ARB_texture_env_add */
/* ----------------------- GL_ARB_texture_env_combine ---------------------- */
#ifndef GL_ARB_texture_env_combine
#endif /* GL_ARB_texture_env_combine */
/* ---------------------- GL_ARB_texture_env_crossbar ---------------------- */
#ifndef GL_ARB_texture_env_crossbar
#endif /* GL_ARB_texture_env_crossbar */
/* ------------------------ GL_ARB_texture_env_dot3 ------------------------ */
#ifndef GL_ARB_texture_env_dot3
#endif /* GL_ARB_texture_env_dot3 */
/* ------------------- GL_ARB_texture_filter_anisotropic ------------------- */
#ifndef GL_ARB_texture_filter_anisotropic
#endif /* GL_ARB_texture_filter_anisotropic */
/* ---------------------- GL_ARB_texture_filter_minmax --------------------- */
#ifndef GL_ARB_texture_filter_minmax
#endif /* GL_ARB_texture_filter_minmax */
/* -------------------------- GL_ARB_texture_float ------------------------- */
#ifndef GL_ARB_texture_float
#endif /* GL_ARB_texture_float */
/* ------------------------- GL_ARB_texture_gather ------------------------- */
#ifndef GL_ARB_texture_gather
#endif /* GL_ARB_texture_gather */
/* ------------------ GL_ARB_texture_mirror_clamp_to_edge ------------------ */
#ifndef GL_ARB_texture_mirror_clamp_to_edge
#endif /* GL_ARB_texture_mirror_clamp_to_edge */
/* --------------------- GL_ARB_texture_mirrored_repeat -------------------- */
#ifndef GL_ARB_texture_mirrored_repeat
#endif /* GL_ARB_texture_mirrored_repeat */
/* ----------------------- GL_ARB_texture_multisample ---------------------- */
#ifndef GL_ARB_texture_multisample
#endif /* GL_ARB_texture_multisample */
/* -------------------- GL_ARB_texture_non_power_of_two -------------------- */
#ifndef GL_ARB_texture_non_power_of_two
#endif /* GL_ARB_texture_non_power_of_two */
/* ---------------------- GL_ARB_texture_query_levels ---------------------- */
#ifndef GL_ARB_texture_query_levels
#endif /* GL_ARB_texture_query_levels */
/* ------------------------ GL_ARB_texture_query_lod ----------------------- */
#ifndef GL_ARB_texture_query_lod
#endif /* GL_ARB_texture_query_lod */
/* ------------------------ GL_ARB_texture_rectangle ----------------------- */
#ifndef GL_ARB_texture_rectangle
#endif /* GL_ARB_texture_rectangle */
/* --------------------------- GL_ARB_texture_rg --------------------------- */
#ifndef GL_ARB_texture_rg
#endif /* GL_ARB_texture_rg */
/* ----------------------- GL_ARB_texture_rgb10_a2ui ----------------------- */
#ifndef GL_ARB_texture_rgb10_a2ui
#endif /* GL_ARB_texture_rgb10_a2ui */
/* ------------------------ GL_ARB_texture_stencil8 ------------------------ */
#ifndef GL_ARB_texture_stencil8
#endif /* GL_ARB_texture_stencil8 */
/* ------------------------- GL_ARB_texture_storage ------------------------ */
#ifndef GL_ARB_texture_storage
#endif /* GL_ARB_texture_storage */
/* ------------------- GL_ARB_texture_storage_multisample ------------------ */
#ifndef GL_ARB_texture_storage_multisample
#endif /* GL_ARB_texture_storage_multisample */
/* ------------------------- GL_ARB_texture_swizzle ------------------------ */
#ifndef GL_ARB_texture_swizzle
#endif /* GL_ARB_texture_swizzle */
/* -------------------------- GL_ARB_texture_view -------------------------- */
#ifndef GL_ARB_texture_view
#endif /* GL_ARB_texture_view */
/* --------------------------- GL_ARB_timer_query -------------------------- */
#ifndef GL_ARB_timer_query
#endif /* GL_ARB_timer_query */
/* ----------------------- GL_ARB_transform_feedback2 ---------------------- */
#ifndef GL_ARB_transform_feedback2
#endif /* GL_ARB_transform_feedback2 */
/* ----------------------- GL_ARB_transform_feedback3 ---------------------- */
#ifndef GL_ARB_transform_feedback3
#endif /* GL_ARB_transform_feedback3 */
/* ------------------ GL_ARB_transform_feedback_instanced ------------------ */
#ifndef GL_ARB_transform_feedback_instanced
#endif /* GL_ARB_transform_feedback_instanced */
/* ---------------- GL_ARB_transform_feedback_overflow_query --------------- */
#ifndef GL_ARB_transform_feedback_overflow_query
#endif /* GL_ARB_transform_feedback_overflow_query */
/* ------------------------ GL_ARB_transpose_matrix ------------------------ */
#ifndef GL_ARB_transpose_matrix
#endif /* GL_ARB_transpose_matrix */
/* ---------------------- GL_ARB_uniform_buffer_object --------------------- */
#ifndef GL_ARB_uniform_buffer_object
#endif /* GL_ARB_uniform_buffer_object */
/* ------------------------ GL_ARB_vertex_array_bgra ----------------------- */
#ifndef GL_ARB_vertex_array_bgra
#endif /* GL_ARB_vertex_array_bgra */
/* ----------------------- GL_ARB_vertex_array_object ---------------------- */
#ifndef GL_ARB_vertex_array_object
#endif /* GL_ARB_vertex_array_object */
/* ----------------------- GL_ARB_vertex_attrib_64bit ---------------------- */
#ifndef GL_ARB_vertex_attrib_64bit
#endif /* GL_ARB_vertex_attrib_64bit */
/* ---------------------- GL_ARB_vertex_attrib_binding --------------------- */
#ifndef GL_ARB_vertex_attrib_binding
#endif /* GL_ARB_vertex_attrib_binding */
/* -------------------------- GL_ARB_vertex_blend -------------------------- */
#ifndef GL_ARB_vertex_blend
#endif /* GL_ARB_vertex_blend */
/* ---------------------- GL_ARB_vertex_buffer_object ---------------------- */
#ifndef GL_ARB_vertex_buffer_object
typedef ptrdiff_t GLintptrARB;
typedef ptrdiff_t GLsizeiptrARB;
#endif /* GL_ARB_vertex_buffer_object */
/* ------------------------- GL_ARB_vertex_program ------------------------- */
#ifndef GL_ARB_vertex_program
#endif /* GL_ARB_vertex_program */
/* -------------------------- GL_ARB_vertex_shader ------------------------- */
#ifndef GL_ARB_vertex_shader
#endif /* GL_ARB_vertex_shader */
/* ------------------- GL_ARB_vertex_type_10f_11f_11f_rev ------------------ */
#ifndef GL_ARB_vertex_type_10f_11f_11f_rev
#endif /* GL_ARB_vertex_type_10f_11f_11f_rev */
/* ------------------- GL_ARB_vertex_type_2_10_10_10_rev ------------------- */
#ifndef GL_ARB_vertex_type_2_10_10_10_rev
#endif /* GL_ARB_vertex_type_2_10_10_10_rev */
/* ------------------------- GL_ARB_viewport_array ------------------------- */
#ifndef GL_ARB_viewport_array
#endif /* GL_ARB_viewport_array */
/* --------------------------- GL_ARB_window_pos --------------------------- */
#ifndef GL_ARB_window_pos
#endif /* GL_ARB_window_pos */
/* ----------------------- GL_ARM_mali_program_binary ---------------------- */
#ifndef GL_ARM_mali_program_binary
#endif /* GL_ARM_mali_program_binary */
/* ----------------------- GL_ARM_mali_shader_binary ----------------------- */
#ifndef GL_ARM_mali_shader_binary
#endif /* GL_ARM_mali_shader_binary */
/* ------------------------------ GL_ARM_rgba8 ----------------------------- */
#ifndef GL_ARM_rgba8
#endif /* GL_ARM_rgba8 */
/* -------------------- GL_ARM_shader_framebuffer_fetch -------------------- */
#ifndef GL_ARM_shader_framebuffer_fetch
#endif /* GL_ARM_shader_framebuffer_fetch */
/* ------------- GL_ARM_shader_framebuffer_fetch_depth_stencil ------------- */
#ifndef GL_ARM_shader_framebuffer_fetch_depth_stencil
#endif /* GL_ARM_shader_framebuffer_fetch_depth_stencil */
/* ------------------------- GL_ATIX_point_sprites ------------------------- */
#ifndef GL_ATIX_point_sprites
#endif /* GL_ATIX_point_sprites */
/* ---------------------- GL_ATIX_texture_env_combine3 --------------------- */
#ifndef GL_ATIX_texture_env_combine3
#endif /* GL_ATIX_texture_env_combine3 */
/* ----------------------- GL_ATIX_texture_env_route ----------------------- */
#ifndef GL_ATIX_texture_env_route
#endif /* GL_ATIX_texture_env_route */
/* ---------------- GL_ATIX_vertex_shader_output_point_size ---------------- */
#ifndef GL_ATIX_vertex_shader_output_point_size
#endif /* GL_ATIX_vertex_shader_output_point_size */
/* -------------------------- GL_ATI_draw_buffers -------------------------- */
#ifndef GL_ATI_draw_buffers
#endif /* GL_ATI_draw_buffers */
/* -------------------------- GL_ATI_element_array ------------------------- */
#ifndef GL_ATI_element_array
#endif /* GL_ATI_element_array */
/* ------------------------- GL_ATI_envmap_bumpmap ------------------------- */
#ifndef GL_ATI_envmap_bumpmap
#endif /* GL_ATI_envmap_bumpmap */
/* ------------------------- GL_ATI_fragment_shader ------------------------ */
#ifndef GL_ATI_fragment_shader
#endif /* GL_ATI_fragment_shader */
/* ------------------------ GL_ATI_map_object_buffer ----------------------- */
#ifndef GL_ATI_map_object_buffer
#endif /* GL_ATI_map_object_buffer */
/* ----------------------------- GL_ATI_meminfo ---------------------------- */
#ifndef GL_ATI_meminfo
#endif /* GL_ATI_meminfo */
/* -------------------------- GL_ATI_pn_triangles -------------------------- */
#ifndef GL_ATI_pn_triangles
#endif /* GL_ATI_pn_triangles */
/* ------------------------ GL_ATI_separate_stencil ------------------------ */
#ifndef GL_ATI_separate_stencil
#endif /* GL_ATI_separate_stencil */
/* ----------------------- GL_ATI_shader_texture_lod ----------------------- */
#ifndef GL_ATI_shader_texture_lod
#endif /* GL_ATI_shader_texture_lod */
/* ---------------------- GL_ATI_text_fragment_shader ---------------------- */
#ifndef GL_ATI_text_fragment_shader
#endif /* GL_ATI_text_fragment_shader */
/* --------------------- GL_ATI_texture_compression_3dc -------------------- */
#ifndef GL_ATI_texture_compression_3dc
#endif /* GL_ATI_texture_compression_3dc */
/* ---------------------- GL_ATI_texture_env_combine3 ---------------------- */
#ifndef GL_ATI_texture_env_combine3
#endif /* GL_ATI_texture_env_combine3 */
/* -------------------------- GL_ATI_texture_float ------------------------- */
#ifndef GL_ATI_texture_float
#endif /* GL_ATI_texture_float */
/* ----------------------- GL_ATI_texture_mirror_once ---------------------- */
#ifndef GL_ATI_texture_mirror_once
#endif /* GL_ATI_texture_mirror_once */
/* ----------------------- GL_ATI_vertex_array_object ---------------------- */
#ifndef GL_ATI_vertex_array_object
#endif /* GL_ATI_vertex_array_object */
/* ------------------- GL_ATI_vertex_attrib_array_object ------------------- */
#ifndef GL_ATI_vertex_attrib_array_object
#endif /* GL_ATI_vertex_attrib_array_object */
/* ------------------------- GL_ATI_vertex_streams ------------------------- */
#ifndef GL_ATI_vertex_streams
#endif /* GL_ATI_vertex_streams */
/* -------------------- GL_EGL_KHR_context_flush_control ------------------- */
#ifndef GL_EGL_KHR_context_flush_control
#endif /* GL_EGL_KHR_context_flush_control */
/* ---------------- GL_EGL_NV_robustness_video_memory_purge ---------------- */
#ifndef GL_EGL_NV_robustness_video_memory_purge
#endif /* GL_EGL_NV_robustness_video_memory_purge */
/* --------------------------- GL_EXT_422_pixels --------------------------- */
#ifndef GL_EXT_422_pixels
#endif /* GL_EXT_422_pixels */
/* ---------------------------- GL_EXT_Cg_shader --------------------------- */
#ifndef GL_EXT_Cg_shader
#endif /* GL_EXT_Cg_shader */
/* ------------------------- GL_EXT_EGL_image_array ------------------------ */
#ifndef GL_EXT_EGL_image_array
#endif /* GL_EXT_EGL_image_array */
/* --------------------------- GL_EXT_YUV_target --------------------------- */
#ifndef GL_EXT_YUV_target
#endif /* GL_EXT_YUV_target */
/* ------------------------------ GL_EXT_abgr ------------------------------ */
#ifndef GL_EXT_abgr
#endif /* GL_EXT_abgr */
/* -------------------------- GL_EXT_base_instance ------------------------- */
#ifndef GL_EXT_base_instance
#endif /* GL_EXT_base_instance */
/* ------------------------------ GL_EXT_bgra ------------------------------ */
#ifndef GL_EXT_bgra
#endif /* GL_EXT_bgra */
/* ------------------------ GL_EXT_bindable_uniform ------------------------ */
#ifndef GL_EXT_bindable_uniform
#endif /* GL_EXT_bindable_uniform */
/* --------------------------- GL_EXT_blend_color -------------------------- */
#ifndef GL_EXT_blend_color
#endif /* GL_EXT_blend_color */
/* --------------------- GL_EXT_blend_equation_separate -------------------- */
#ifndef GL_EXT_blend_equation_separate
#endif /* GL_EXT_blend_equation_separate */
/* ----------------------- GL_EXT_blend_func_extended ---------------------- */
#ifndef GL_EXT_blend_func_extended
#endif /* GL_EXT_blend_func_extended */
/* ----------------------- GL_EXT_blend_func_separate ---------------------- */
#ifndef GL_EXT_blend_func_separate
#endif /* GL_EXT_blend_func_separate */
/* ------------------------- GL_EXT_blend_logic_op ------------------------- */
#ifndef GL_EXT_blend_logic_op
#endif /* GL_EXT_blend_logic_op */
/* -------------------------- GL_EXT_blend_minmax -------------------------- */
#ifndef GL_EXT_blend_minmax
#endif /* GL_EXT_blend_minmax */
/* ------------------------- GL_EXT_blend_subtract ------------------------- */
#ifndef GL_EXT_blend_subtract
#endif /* GL_EXT_blend_subtract */
/* ------------------------- GL_EXT_buffer_storage ------------------------- */
#ifndef GL_EXT_buffer_storage
#endif /* GL_EXT_buffer_storage */
/* -------------------------- GL_EXT_clear_texture ------------------------- */
#ifndef GL_EXT_clear_texture
#endif /* GL_EXT_clear_texture */
/* ----------------------- GL_EXT_clip_cull_distance ----------------------- */
#ifndef GL_EXT_clip_cull_distance
#endif /* GL_EXT_clip_cull_distance */
/* ------------------------ GL_EXT_clip_volume_hint ------------------------ */
#ifndef GL_EXT_clip_volume_hint
#endif /* GL_EXT_clip_volume_hint */
/* ------------------------------ GL_EXT_cmyka ----------------------------- */
#ifndef GL_EXT_cmyka
#endif /* GL_EXT_cmyka */
/* ----------------------- GL_EXT_color_buffer_float ----------------------- */
#ifndef GL_EXT_color_buffer_float
#endif /* GL_EXT_color_buffer_float */
/* --------------------- GL_EXT_color_buffer_half_float -------------------- */
#ifndef GL_EXT_color_buffer_half_float
#endif /* GL_EXT_color_buffer_half_float */
/* ------------------------- GL_EXT_color_subtable ------------------------- */
#ifndef GL_EXT_color_subtable
#endif /* GL_EXT_color_subtable */
/* ---------------------- GL_EXT_compiled_vertex_array --------------------- */
#ifndef GL_EXT_compiled_vertex_array
#endif /* GL_EXT_compiled_vertex_array */
/* ---------------- GL_EXT_compressed_ETC1_RGB8_sub_texture ---------------- */
#ifndef GL_EXT_compressed_ETC1_RGB8_sub_texture
#endif /* GL_EXT_compressed_ETC1_RGB8_sub_texture */
/* ----------------------- GL_EXT_conservative_depth ----------------------- */
#ifndef GL_EXT_conservative_depth
#endif /* GL_EXT_conservative_depth */
/* --------------------------- GL_EXT_convolution -------------------------- */
#ifndef GL_EXT_convolution
#endif /* GL_EXT_convolution */
/* ------------------------ GL_EXT_coordinate_frame ------------------------ */
#ifndef GL_EXT_coordinate_frame
#endif /* GL_EXT_coordinate_frame */
/* --------------------------- GL_EXT_copy_image --------------------------- */
#ifndef GL_EXT_copy_image
#endif /* GL_EXT_copy_image */
/* -------------------------- GL_EXT_copy_texture -------------------------- */
#ifndef GL_EXT_copy_texture
#endif /* GL_EXT_copy_texture */
/* --------------------------- GL_EXT_cull_vertex -------------------------- */
#ifndef GL_EXT_cull_vertex
#endif /* GL_EXT_cull_vertex */
/* --------------------------- GL_EXT_debug_label -------------------------- */
#ifndef GL_EXT_debug_label
#endif /* GL_EXT_debug_label */
/* -------------------------- GL_EXT_debug_marker -------------------------- */
#ifndef GL_EXT_debug_marker
#endif /* GL_EXT_debug_marker */
/* ------------------------ GL_EXT_depth_bounds_test ----------------------- */
#ifndef GL_EXT_depth_bounds_test
#endif /* GL_EXT_depth_bounds_test */
/* ----------------------- GL_EXT_direct_state_access ---------------------- */
#ifndef GL_EXT_direct_state_access
#endif /* GL_EXT_direct_state_access */
/* ----------------------- GL_EXT_discard_framebuffer ---------------------- */
#ifndef GL_EXT_discard_framebuffer
#endif /* GL_EXT_discard_framebuffer */
/* -------------------------- GL_EXT_draw_buffers -------------------------- */
#ifndef GL_EXT_draw_buffers
#endif /* GL_EXT_draw_buffers */
/* -------------------------- GL_EXT_draw_buffers2 ------------------------- */
#ifndef GL_EXT_draw_buffers2
#endif /* GL_EXT_draw_buffers2 */
/* ---------------------- GL_EXT_draw_buffers_indexed ---------------------- */
#ifndef GL_EXT_draw_buffers_indexed
#endif /* GL_EXT_draw_buffers_indexed */
/* -------------------- GL_EXT_draw_elements_base_vertex ------------------- */
#ifndef GL_EXT_draw_elements_base_vertex
#endif /* GL_EXT_draw_elements_base_vertex */
/* ------------------------- GL_EXT_draw_instanced ------------------------- */
#ifndef GL_EXT_draw_instanced
#endif /* GL_EXT_draw_instanced */
/* ----------------------- GL_EXT_draw_range_elements ---------------------- */
#ifndef GL_EXT_draw_range_elements
#endif /* GL_EXT_draw_range_elements */
/* ------------------------- GL_EXT_external_buffer ------------------------ */
#ifndef GL_EXT_external_buffer
typedef void* GLeglClientBufferEXT;
#endif /* GL_EXT_external_buffer */
/* --------------------------- GL_EXT_float_blend -------------------------- */
#ifndef GL_EXT_float_blend
#endif /* GL_EXT_float_blend */
/* ---------------------------- GL_EXT_fog_coord --------------------------- */
#ifndef GL_EXT_fog_coord
#endif /* GL_EXT_fog_coord */
/* --------------------------- GL_EXT_frag_depth --------------------------- */
#ifndef GL_EXT_frag_depth
#endif /* GL_EXT_frag_depth */
/* ------------------------ GL_EXT_fragment_lighting ----------------------- */
#ifndef GL_EXT_fragment_lighting
#endif /* GL_EXT_fragment_lighting */
/* ------------------------ GL_EXT_framebuffer_blit ------------------------ */
#ifndef GL_EXT_framebuffer_blit
#endif /* GL_EXT_framebuffer_blit */
/* --------------------- GL_EXT_framebuffer_multisample -------------------- */
#ifndef GL_EXT_framebuffer_multisample
#endif /* GL_EXT_framebuffer_multisample */
/* --------------- GL_EXT_framebuffer_multisample_blit_scaled -------------- */
#ifndef GL_EXT_framebuffer_multisample_blit_scaled
#endif /* GL_EXT_framebuffer_multisample_blit_scaled */
/* ----------------------- GL_EXT_framebuffer_object ----------------------- */
#ifndef GL_EXT_framebuffer_object
#endif /* GL_EXT_framebuffer_object */
/* ------------------------ GL_EXT_framebuffer_sRGB ------------------------ */
#ifndef GL_EXT_framebuffer_sRGB
#endif /* GL_EXT_framebuffer_sRGB */
/* ----------------------- GL_EXT_geometry_point_size ---------------------- */
#ifndef GL_EXT_geometry_point_size
#endif /* GL_EXT_geometry_point_size */
/* ------------------------- GL_EXT_geometry_shader ------------------------ */
#ifndef GL_EXT_geometry_shader
#endif /* GL_EXT_geometry_shader */
/* ------------------------ GL_EXT_geometry_shader4 ------------------------ */
#ifndef GL_EXT_geometry_shader4
#endif /* GL_EXT_geometry_shader4 */
/* --------------------- GL_EXT_gpu_program_parameters --------------------- */
#ifndef GL_EXT_gpu_program_parameters
#endif /* GL_EXT_gpu_program_parameters */
/* --------------------------- GL_EXT_gpu_shader4 -------------------------- */
#ifndef GL_EXT_gpu_shader4
#endif /* GL_EXT_gpu_shader4 */
/* --------------------------- GL_EXT_gpu_shader5 -------------------------- */
#ifndef GL_EXT_gpu_shader5
#endif /* GL_EXT_gpu_shader5 */
/* ---------------------------- GL_EXT_histogram --------------------------- */
#ifndef GL_EXT_histogram
#endif /* GL_EXT_histogram */
/* ----------------------- GL_EXT_index_array_formats ---------------------- */
#ifndef GL_EXT_index_array_formats
#endif /* GL_EXT_index_array_formats */
/* --------------------------- GL_EXT_index_func --------------------------- */
#ifndef GL_EXT_index_func
#endif /* GL_EXT_index_func */
/* ------------------------- GL_EXT_index_material ------------------------- */
#ifndef GL_EXT_index_material
#endif /* GL_EXT_index_material */
/* -------------------------- GL_EXT_index_texture ------------------------- */
#ifndef GL_EXT_index_texture
#endif /* GL_EXT_index_texture */
/* ------------------------ GL_EXT_instanced_arrays ------------------------ */
#ifndef GL_EXT_instanced_arrays
#endif /* GL_EXT_instanced_arrays */
/* -------------------------- GL_EXT_light_texture ------------------------- */
#ifndef GL_EXT_light_texture
#endif /* GL_EXT_light_texture */
/* ------------------------ GL_EXT_map_buffer_range ------------------------ */
#ifndef GL_EXT_map_buffer_range
#endif /* GL_EXT_map_buffer_range */
/* -------------------------- GL_EXT_memory_object ------------------------- */
#ifndef GL_EXT_memory_object
#endif /* GL_EXT_memory_object */
/* ------------------------ GL_EXT_memory_object_fd ------------------------ */
#ifndef GL_EXT_memory_object_fd
#endif /* GL_EXT_memory_object_fd */
/* ----------------------- GL_EXT_memory_object_win32 ---------------------- */
#ifndef GL_EXT_memory_object_win32
#endif /* GL_EXT_memory_object_win32 */
/* ------------------------- GL_EXT_misc_attribute ------------------------- */
#ifndef GL_EXT_misc_attribute
#endif /* GL_EXT_misc_attribute */
/* ------------------------ GL_EXT_multi_draw_arrays ----------------------- */
#ifndef GL_EXT_multi_draw_arrays
#endif /* GL_EXT_multi_draw_arrays */
/* ----------------------- GL_EXT_multi_draw_indirect ---------------------- */
#ifndef GL_EXT_multi_draw_indirect
#endif /* GL_EXT_multi_draw_indirect */
/* ------------------------ GL_EXT_multiple_textures ----------------------- */
#ifndef GL_EXT_multiple_textures
#endif /* GL_EXT_multiple_textures */
/* --------------------------- GL_EXT_multisample -------------------------- */
#ifndef GL_EXT_multisample
#endif /* GL_EXT_multisample */
/* -------------------- GL_EXT_multisample_compatibility ------------------- */
#ifndef GL_EXT_multisample_compatibility
#endif /* GL_EXT_multisample_compatibility */
/* ----------------- GL_EXT_multisampled_render_to_texture ----------------- */
#ifndef GL_EXT_multisampled_render_to_texture
#endif /* GL_EXT_multisampled_render_to_texture */
/* ----------------- GL_EXT_multisampled_render_to_texture2 ---------------- */
#ifndef GL_EXT_multisampled_render_to_texture2
#endif /* GL_EXT_multisampled_render_to_texture2 */
/* --------------------- GL_EXT_multiview_draw_buffers --------------------- */
#ifndef GL_EXT_multiview_draw_buffers
#endif /* GL_EXT_multiview_draw_buffers */
/* ---------------------- GL_EXT_packed_depth_stencil ---------------------- */
#ifndef GL_EXT_packed_depth_stencil
#endif /* GL_EXT_packed_depth_stencil */
/* -------------------------- GL_EXT_packed_float -------------------------- */
#ifndef GL_EXT_packed_float
#endif /* GL_EXT_packed_float */
/* -------------------------- GL_EXT_packed_pixels ------------------------- */
#ifndef GL_EXT_packed_pixels
#endif /* GL_EXT_packed_pixels */
/* ------------------------ GL_EXT_paletted_texture ------------------------ */
#ifndef GL_EXT_paletted_texture
#endif /* GL_EXT_paletted_texture */
/* ----------------------- GL_EXT_pixel_buffer_object ---------------------- */
#ifndef GL_EXT_pixel_buffer_object
#endif /* GL_EXT_pixel_buffer_object */
/* ------------------------- GL_EXT_pixel_transform ------------------------ */
#ifndef GL_EXT_pixel_transform
#endif /* GL_EXT_pixel_transform */
/* ------------------- GL_EXT_pixel_transform_color_table ------------------ */
#ifndef GL_EXT_pixel_transform_color_table
#endif /* GL_EXT_pixel_transform_color_table */
/* ------------------------ GL_EXT_point_parameters ------------------------ */
#ifndef GL_EXT_point_parameters
#endif /* GL_EXT_point_parameters */
/* ------------------------- GL_EXT_polygon_offset ------------------------- */
#ifndef GL_EXT_polygon_offset
#endif /* GL_EXT_polygon_offset */
/* ---------------------- GL_EXT_polygon_offset_clamp ---------------------- */
#ifndef GL_EXT_polygon_offset_clamp
#endif /* GL_EXT_polygon_offset_clamp */
/* ----------------------- GL_EXT_post_depth_coverage ---------------------- */
#ifndef GL_EXT_post_depth_coverage
#endif /* GL_EXT_post_depth_coverage */
/* ------------------------ GL_EXT_provoking_vertex ------------------------ */
#ifndef GL_EXT_provoking_vertex
#endif /* GL_EXT_provoking_vertex */
/* --------------------------- GL_EXT_pvrtc_sRGB --------------------------- */
#ifndef GL_EXT_pvrtc_sRGB
#endif /* GL_EXT_pvrtc_sRGB */
/* ----------------------- GL_EXT_raster_multisample ----------------------- */
#ifndef GL_EXT_raster_multisample
#endif /* GL_EXT_raster_multisample */
/* ------------------------ GL_EXT_read_format_bgra ------------------------ */
#ifndef GL_EXT_read_format_bgra
#endif /* GL_EXT_read_format_bgra */
/* -------------------------- GL_EXT_render_snorm -------------------------- */
#ifndef GL_EXT_render_snorm
#endif /* GL_EXT_render_snorm */
/* ------------------------- GL_EXT_rescale_normal ------------------------- */
#ifndef GL_EXT_rescale_normal
#endif /* GL_EXT_rescale_normal */
/* ------------------------------ GL_EXT_sRGB ------------------------------ */
#ifndef GL_EXT_sRGB
#endif /* GL_EXT_sRGB */
/* ----------------------- GL_EXT_sRGB_write_control ----------------------- */
#ifndef GL_EXT_sRGB_write_control
#endif /* GL_EXT_sRGB_write_control */
/* -------------------------- GL_EXT_scene_marker -------------------------- */
#ifndef GL_EXT_scene_marker
#endif /* GL_EXT_scene_marker */
/* ------------------------- GL_EXT_secondary_color ------------------------ */
#ifndef GL_EXT_secondary_color
#endif /* GL_EXT_secondary_color */
/* ---------------------------- GL_EXT_semaphore --------------------------- */
#ifndef GL_EXT_semaphore
#endif /* GL_EXT_semaphore */
/* -------------------------- GL_EXT_semaphore_fd -------------------------- */
#ifndef GL_EXT_semaphore_fd
#endif /* GL_EXT_semaphore_fd */
/* ------------------------- GL_EXT_semaphore_win32 ------------------------ */
#ifndef GL_EXT_semaphore_win32
#endif /* GL_EXT_semaphore_win32 */
/* --------------------- GL_EXT_separate_shader_objects -------------------- */
#ifndef GL_EXT_separate_shader_objects
#endif /* GL_EXT_separate_shader_objects */
/* --------------------- GL_EXT_separate_specular_color -------------------- */
#ifndef GL_EXT_separate_specular_color
#endif /* GL_EXT_separate_specular_color */
/* -------------------- GL_EXT_shader_framebuffer_fetch -------------------- */
#ifndef GL_EXT_shader_framebuffer_fetch
#endif /* GL_EXT_shader_framebuffer_fetch */
/* ------------------------ GL_EXT_shader_group_vote ----------------------- */
#ifndef GL_EXT_shader_group_vote
#endif /* GL_EXT_shader_group_vote */
/* ------------------- GL_EXT_shader_image_load_formatted ------------------ */
#ifndef GL_EXT_shader_image_load_formatted
#endif /* GL_EXT_shader_image_load_formatted */
/* --------------------- GL_EXT_shader_image_load_store -------------------- */
#ifndef GL_EXT_shader_image_load_store
#endif /* GL_EXT_shader_image_load_store */
/* ------------------- GL_EXT_shader_implicit_conversions ------------------ */
#ifndef GL_EXT_shader_implicit_conversions
#endif /* GL_EXT_shader_implicit_conversions */
/* ----------------------- GL_EXT_shader_integer_mix ----------------------- */
#ifndef GL_EXT_shader_integer_mix
#endif /* GL_EXT_shader_integer_mix */
/* ------------------------ GL_EXT_shader_io_blocks ------------------------ */
#ifndef GL_EXT_shader_io_blocks
#endif /* GL_EXT_shader_io_blocks */
/* ------------- GL_EXT_shader_non_constant_global_initializers ------------ */
#ifndef GL_EXT_shader_non_constant_global_initializers
#endif /* GL_EXT_shader_non_constant_global_initializers */
/* ------------------- GL_EXT_shader_pixel_local_storage ------------------- */
#ifndef GL_EXT_shader_pixel_local_storage
#endif /* GL_EXT_shader_pixel_local_storage */
/* ------------------- GL_EXT_shader_pixel_local_storage2 ------------------ */
#ifndef GL_EXT_shader_pixel_local_storage2
#endif /* GL_EXT_shader_pixel_local_storage2 */
/* ----------------------- GL_EXT_shader_texture_lod ----------------------- */
#ifndef GL_EXT_shader_texture_lod
#endif /* GL_EXT_shader_texture_lod */
/* -------------------------- GL_EXT_shadow_funcs -------------------------- */
#ifndef GL_EXT_shadow_funcs
#endif /* GL_EXT_shadow_funcs */
/* ------------------------- GL_EXT_shadow_samplers ------------------------ */
#ifndef GL_EXT_shadow_samplers
#endif /* GL_EXT_shadow_samplers */
/* --------------------- GL_EXT_shared_texture_palette --------------------- */
#ifndef GL_EXT_shared_texture_palette
#endif /* GL_EXT_shared_texture_palette */
/* ------------------------- GL_EXT_sparse_texture ------------------------- */
#ifndef GL_EXT_sparse_texture
#endif /* GL_EXT_sparse_texture */
/* ------------------------- GL_EXT_sparse_texture2 ------------------------ */
#ifndef GL_EXT_sparse_texture2
#endif /* GL_EXT_sparse_texture2 */
/* ------------------------ GL_EXT_stencil_clear_tag ----------------------- */
#ifndef GL_EXT_stencil_clear_tag
#endif /* GL_EXT_stencil_clear_tag */
/* ------------------------ GL_EXT_stencil_two_side ------------------------ */
#ifndef GL_EXT_stencil_two_side
#endif /* GL_EXT_stencil_two_side */
/* -------------------------- GL_EXT_stencil_wrap -------------------------- */
#ifndef GL_EXT_stencil_wrap
#endif /* GL_EXT_stencil_wrap */
/* --------------------------- GL_EXT_subtexture --------------------------- */
#ifndef GL_EXT_subtexture
#endif /* GL_EXT_subtexture */
/* ----------------------------- GL_EXT_texture ---------------------------- */
#ifndef GL_EXT_texture
#endif /* GL_EXT_texture */
/* ---------------------------- GL_EXT_texture3D --------------------------- */
#ifndef GL_EXT_texture3D
#endif /* GL_EXT_texture3D */
/* -------------------------- GL_EXT_texture_array ------------------------- */
#ifndef GL_EXT_texture_array
#endif /* GL_EXT_texture_array */
/* ---------------------- GL_EXT_texture_buffer_object --------------------- */
#ifndef GL_EXT_texture_buffer_object
#endif /* GL_EXT_texture_buffer_object */
/* -------------- GL_EXT_texture_compression_astc_decode_mode -------------- */
#ifndef GL_EXT_texture_compression_astc_decode_mode
#endif /* GL_EXT_texture_compression_astc_decode_mode */
/* ----------- GL_EXT_texture_compression_astc_decode_mode_rgb9e5 ---------- */
#ifndef GL_EXT_texture_compression_astc_decode_mode_rgb9e5
#endif /* GL_EXT_texture_compression_astc_decode_mode_rgb9e5 */
/* -------------------- GL_EXT_texture_compression_bptc -------------------- */
#ifndef GL_EXT_texture_compression_bptc
#endif /* GL_EXT_texture_compression_bptc */
/* -------------------- GL_EXT_texture_compression_dxt1 -------------------- */
#ifndef GL_EXT_texture_compression_dxt1
#endif /* GL_EXT_texture_compression_dxt1 */
/* -------------------- GL_EXT_texture_compression_latc -------------------- */
#ifndef GL_EXT_texture_compression_latc
#endif /* GL_EXT_texture_compression_latc */
/* -------------------- GL_EXT_texture_compression_rgtc -------------------- */
#ifndef GL_EXT_texture_compression_rgtc
#endif /* GL_EXT_texture_compression_rgtc */
/* -------------------- GL_EXT_texture_compression_s3tc -------------------- */
#ifndef GL_EXT_texture_compression_s3tc
#endif /* GL_EXT_texture_compression_s3tc */
/* ------------------------ GL_EXT_texture_cube_map ------------------------ */
#ifndef GL_EXT_texture_cube_map
#endif /* GL_EXT_texture_cube_map */
/* --------------------- GL_EXT_texture_cube_map_array --------------------- */
#ifndef GL_EXT_texture_cube_map_array
#endif /* GL_EXT_texture_cube_map_array */
/* ----------------------- GL_EXT_texture_edge_clamp ----------------------- */
#ifndef GL_EXT_texture_edge_clamp
#endif /* GL_EXT_texture_edge_clamp */
/* --------------------------- GL_EXT_texture_env -------------------------- */
#ifndef GL_EXT_texture_env
#endif /* GL_EXT_texture_env */
/* ------------------------- GL_EXT_texture_env_add ------------------------ */
#ifndef GL_EXT_texture_env_add
#endif /* GL_EXT_texture_env_add */
/* ----------------------- GL_EXT_texture_env_combine ---------------------- */
#ifndef GL_EXT_texture_env_combine
#endif /* GL_EXT_texture_env_combine */
/* ------------------------ GL_EXT_texture_env_dot3 ------------------------ */
#ifndef GL_EXT_texture_env_dot3
#endif /* GL_EXT_texture_env_dot3 */
/* ------------------- GL_EXT_texture_filter_anisotropic ------------------- */
#ifndef GL_EXT_texture_filter_anisotropic
#endif /* GL_EXT_texture_filter_anisotropic */
/* ---------------------- GL_EXT_texture_filter_minmax --------------------- */
#ifndef GL_EXT_texture_filter_minmax
#endif /* GL_EXT_texture_filter_minmax */
/* --------------------- GL_EXT_texture_format_BGRA8888 -------------------- */
#ifndef GL_EXT_texture_format_BGRA8888
#endif /* GL_EXT_texture_format_BGRA8888 */
/* ------------------------- GL_EXT_texture_integer ------------------------ */
#ifndef GL_EXT_texture_integer
#endif /* GL_EXT_texture_integer */
/* ------------------------ GL_EXT_texture_lod_bias ------------------------ */
#ifndef GL_EXT_texture_lod_bias
#endif /* GL_EXT_texture_lod_bias */
/* ---------------------- GL_EXT_texture_mirror_clamp ---------------------- */
#ifndef GL_EXT_texture_mirror_clamp
#endif /* GL_EXT_texture_mirror_clamp */
/* ------------------------- GL_EXT_texture_norm16 ------------------------- */
#ifndef GL_EXT_texture_norm16
#endif /* GL_EXT_texture_norm16 */
/* ------------------------- GL_EXT_texture_object ------------------------- */
#ifndef GL_EXT_texture_object
#endif /* GL_EXT_texture_object */
/* --------------------- GL_EXT_texture_perturb_normal --------------------- */
#ifndef GL_EXT_texture_perturb_normal
#endif /* GL_EXT_texture_perturb_normal */
/* ------------------------ GL_EXT_texture_rectangle ----------------------- */
#ifndef GL_EXT_texture_rectangle
#endif /* GL_EXT_texture_rectangle */
/* --------------------------- GL_EXT_texture_rg --------------------------- */
#ifndef GL_EXT_texture_rg
#endif /* GL_EXT_texture_rg */
/* -------------------------- GL_EXT_texture_sRGB -------------------------- */
#ifndef GL_EXT_texture_sRGB
#endif /* GL_EXT_texture_sRGB */
/* ------------------------- GL_EXT_texture_sRGB_R8 ------------------------ */
#ifndef GL_EXT_texture_sRGB_R8
#endif /* GL_EXT_texture_sRGB_R8 */
/* ------------------------ GL_EXT_texture_sRGB_RG8 ------------------------ */
#ifndef GL_EXT_texture_sRGB_RG8
#endif /* GL_EXT_texture_sRGB_RG8 */
/* ----------------------- GL_EXT_texture_sRGB_decode ---------------------- */
#ifndef GL_EXT_texture_sRGB_decode
#endif /* GL_EXT_texture_sRGB_decode */
/* --------------------- GL_EXT_texture_shared_exponent -------------------- */
#ifndef GL_EXT_texture_shared_exponent
#endif /* GL_EXT_texture_shared_exponent */
/* -------------------------- GL_EXT_texture_snorm ------------------------- */
#ifndef GL_EXT_texture_snorm
#endif /* GL_EXT_texture_snorm */
/* ------------------------- GL_EXT_texture_storage ------------------------ */
#ifndef GL_EXT_texture_storage
#endif /* GL_EXT_texture_storage */
/* ------------------------- GL_EXT_texture_swizzle ------------------------ */
#ifndef GL_EXT_texture_swizzle
#endif /* GL_EXT_texture_swizzle */
/* ------------------- GL_EXT_texture_type_2_10_10_10_REV ------------------ */
#ifndef GL_EXT_texture_type_2_10_10_10_REV
#endif /* GL_EXT_texture_type_2_10_10_10_REV */
/* -------------------------- GL_EXT_texture_view -------------------------- */
#ifndef GL_EXT_texture_view
#endif /* GL_EXT_texture_view */
/* --------------------------- GL_EXT_timer_query -------------------------- */
#ifndef GL_EXT_timer_query
#endif /* GL_EXT_timer_query */
/* ----------------------- GL_EXT_transform_feedback ----------------------- */
#ifndef GL_EXT_transform_feedback
#endif /* GL_EXT_transform_feedback */
/* ------------------------- GL_EXT_unpack_subimage ------------------------ */
#ifndef GL_EXT_unpack_subimage
#endif /* GL_EXT_unpack_subimage */
/* -------------------------- GL_EXT_vertex_array -------------------------- */
#ifndef GL_EXT_vertex_array
#endif /* GL_EXT_vertex_array */
/* ------------------------ GL_EXT_vertex_array_bgra ----------------------- */
#ifndef GL_EXT_vertex_array_bgra
#endif /* GL_EXT_vertex_array_bgra */
/* ----------------------- GL_EXT_vertex_array_setXXX ---------------------- */
#ifndef GL_EXT_vertex_array_setXXX
#endif /* GL_EXT_vertex_array_setXXX */
/* ----------------------- GL_EXT_vertex_attrib_64bit ---------------------- */
#ifndef GL_EXT_vertex_attrib_64bit
#endif /* GL_EXT_vertex_attrib_64bit */
/* -------------------------- GL_EXT_vertex_shader ------------------------- */
#ifndef GL_EXT_vertex_shader
#endif /* GL_EXT_vertex_shader */
/* ------------------------ GL_EXT_vertex_weighting ------------------------ */
#ifndef GL_EXT_vertex_weighting
#endif /* GL_EXT_vertex_weighting */
/* ------------------------ GL_EXT_win32_keyed_mutex ----------------------- */
#ifndef GL_EXT_win32_keyed_mutex
#endif /* GL_EXT_win32_keyed_mutex */
/* ------------------------ GL_EXT_window_rectangles ----------------------- */
#ifndef GL_EXT_window_rectangles
#endif /* GL_EXT_window_rectangles */
/* ------------------------- GL_EXT_x11_sync_object ------------------------ */
#ifndef GL_EXT_x11_sync_object
#endif /* GL_EXT_x11_sync_object */
/* ---------------------- GL_GREMEDY_frame_terminator ---------------------- */
#ifndef GL_GREMEDY_frame_terminator
#endif /* GL_GREMEDY_frame_terminator */
/* ------------------------ GL_GREMEDY_string_marker ----------------------- */
#ifndef GL_GREMEDY_string_marker
#endif /* GL_GREMEDY_string_marker */
/* --------------------- GL_HP_convolution_border_modes -------------------- */
#ifndef GL_HP_convolution_border_modes
#endif /* GL_HP_convolution_border_modes */
/* ------------------------- GL_HP_image_transform ------------------------- */
#ifndef GL_HP_image_transform
#endif /* GL_HP_image_transform */
/* -------------------------- GL_HP_occlusion_test ------------------------- */
#ifndef GL_HP_occlusion_test
#endif /* GL_HP_occlusion_test */
/* ------------------------- GL_HP_texture_lighting ------------------------ */
#ifndef GL_HP_texture_lighting
#endif /* GL_HP_texture_lighting */
/* --------------------------- GL_IBM_cull_vertex -------------------------- */
#ifndef GL_IBM_cull_vertex
#endif /* GL_IBM_cull_vertex */
/* ---------------------- GL_IBM_multimode_draw_arrays --------------------- */
#ifndef GL_IBM_multimode_draw_arrays
#endif /* GL_IBM_multimode_draw_arrays */
/* ------------------------- GL_IBM_rasterpos_clip ------------------------- */
#ifndef GL_IBM_rasterpos_clip
#endif /* GL_IBM_rasterpos_clip */
/* --------------------------- GL_IBM_static_data -------------------------- */
#ifndef GL_IBM_static_data
#endif /* GL_IBM_static_data */
/* --------------------- GL_IBM_texture_mirrored_repeat -------------------- */
#ifndef GL_IBM_texture_mirrored_repeat
#endif /* GL_IBM_texture_mirrored_repeat */
/* ----------------------- GL_IBM_vertex_array_lists ----------------------- */
#ifndef GL_IBM_vertex_array_lists
#endif /* GL_IBM_vertex_array_lists */
/* -------------------------- GL_INGR_color_clamp -------------------------- */
#ifndef GL_INGR_color_clamp
#endif /* GL_INGR_color_clamp */
/* ------------------------- GL_INGR_interlace_read ------------------------ */
#ifndef GL_INGR_interlace_read
#endif /* GL_INGR_interlace_read */
/* ------------------ GL_INTEL_conservative_rasterization ------------------ */
#ifndef GL_INTEL_conservative_rasterization
#endif /* GL_INTEL_conservative_rasterization */
/* ------------------- GL_INTEL_fragment_shader_ordering ------------------- */
#ifndef GL_INTEL_fragment_shader_ordering
#endif /* GL_INTEL_fragment_shader_ordering */
/* ----------------------- GL_INTEL_framebuffer_CMAA ----------------------- */
#ifndef GL_INTEL_framebuffer_CMAA
#endif /* GL_INTEL_framebuffer_CMAA */
/* -------------------------- GL_INTEL_map_texture ------------------------- */
#ifndef GL_INTEL_map_texture
#endif /* GL_INTEL_map_texture */
/* ------------------------ GL_INTEL_parallel_arrays ----------------------- */
#ifndef GL_INTEL_parallel_arrays
#endif /* GL_INTEL_parallel_arrays */
/* ----------------------- GL_INTEL_performance_query ---------------------- */
#ifndef GL_INTEL_performance_query
#endif /* GL_INTEL_performance_query */
/* ------------------------ GL_INTEL_texture_scissor ----------------------- */
#ifndef GL_INTEL_texture_scissor
#endif /* GL_INTEL_texture_scissor */
/* --------------------- GL_KHR_blend_equation_advanced -------------------- */
#ifndef GL_KHR_blend_equation_advanced
#endif /* GL_KHR_blend_equation_advanced */
/* ---------------- GL_KHR_blend_equation_advanced_coherent ---------------- */
#ifndef GL_KHR_blend_equation_advanced_coherent
#endif /* GL_KHR_blend_equation_advanced_coherent */
/* ---------------------- GL_KHR_context_flush_control --------------------- */
#ifndef GL_KHR_context_flush_control
#endif /* GL_KHR_context_flush_control */
/* ------------------------------ GL_KHR_debug ----------------------------- */
#ifndef GL_KHR_debug
#endif /* GL_KHR_debug */
/* ---------------------------- GL_KHR_no_error ---------------------------- */
#ifndef GL_KHR_no_error
#endif /* GL_KHR_no_error */
/* --------------------- GL_KHR_parallel_shader_compile -------------------- */
#ifndef GL_KHR_parallel_shader_compile
#endif /* GL_KHR_parallel_shader_compile */
/* ------------------ GL_KHR_robust_buffer_access_behavior ----------------- */
#ifndef GL_KHR_robust_buffer_access_behavior
#endif /* GL_KHR_robust_buffer_access_behavior */
/* --------------------------- GL_KHR_robustness --------------------------- */
#ifndef GL_KHR_robustness
#endif /* GL_KHR_robustness */
/* ------------------ GL_KHR_texture_compression_astc_hdr ------------------ */
#ifndef GL_KHR_texture_compression_astc_hdr
#endif /* GL_KHR_texture_compression_astc_hdr */
/* ------------------ GL_KHR_texture_compression_astc_ldr ------------------ */
#ifndef GL_KHR_texture_compression_astc_ldr
#endif /* GL_KHR_texture_compression_astc_ldr */
/* --------------- GL_KHR_texture_compression_astc_sliced_3d --------------- */
#ifndef GL_KHR_texture_compression_astc_sliced_3d
#endif /* GL_KHR_texture_compression_astc_sliced_3d */
/* -------------------------- GL_KTX_buffer_region ------------------------- */
#ifndef GL_KTX_buffer_region
#endif /* GL_KTX_buffer_region */
/* ------------------------- GL_MESAX_texture_stack ------------------------ */
#ifndef GL_MESAX_texture_stack
#endif /* GL_MESAX_texture_stack */
/* -------------------------- GL_MESA_pack_invert -------------------------- */
#ifndef GL_MESA_pack_invert
#endif /* GL_MESA_pack_invert */
/* ------------------------- GL_MESA_resize_buffers ------------------------ */
#ifndef GL_MESA_resize_buffers
#endif /* GL_MESA_resize_buffers */
/* -------------------- GL_MESA_shader_integer_functions ------------------- */
#ifndef GL_MESA_shader_integer_functions
#endif /* GL_MESA_shader_integer_functions */
/* --------------------------- GL_MESA_window_pos -------------------------- */
#ifndef GL_MESA_window_pos
#endif /* GL_MESA_window_pos */
/* ------------------------- GL_MESA_ycbcr_texture ------------------------- */
#ifndef GL_MESA_ycbcr_texture
#endif /* GL_MESA_ycbcr_texture */
/* ----------- GL_NVX_blend_equation_advanced_multi_draw_buffers ----------- */
#ifndef GL_NVX_blend_equation_advanced_multi_draw_buffers
#endif /* GL_NVX_blend_equation_advanced_multi_draw_buffers */
/* ----------------------- GL_NVX_conditional_render ----------------------- */
#ifndef GL_NVX_conditional_render
#endif /* GL_NVX_conditional_render */
/* ------------------------- GL_NVX_gpu_memory_info ------------------------ */
#ifndef GL_NVX_gpu_memory_info
#endif /* GL_NVX_gpu_memory_info */
/* ---------------------- GL_NVX_linked_gpu_multicast ---------------------- */
#ifndef GL_NVX_linked_gpu_multicast
#endif /* GL_NVX_linked_gpu_multicast */
/* ------------------------ GL_NV_3dvision_settings ------------------------ */
#ifndef GL_NV_3dvision_settings
#endif /* GL_NV_3dvision_settings */
/* ------------------- GL_NV_EGL_stream_consumer_external ------------------ */
#ifndef GL_NV_EGL_stream_consumer_external
#endif /* GL_NV_EGL_stream_consumer_external */
/* ----------------- GL_NV_alpha_to_coverage_dither_control ---------------- */
#ifndef GL_NV_alpha_to_coverage_dither_control
#endif /* GL_NV_alpha_to_coverage_dither_control */
/* ------------------------------- GL_NV_bgr ------------------------------- */
#ifndef GL_NV_bgr
#endif /* GL_NV_bgr */
/* ------------------- GL_NV_bindless_multi_draw_indirect ------------------ */
#ifndef GL_NV_bindless_multi_draw_indirect
#endif /* GL_NV_bindless_multi_draw_indirect */
/* ---------------- GL_NV_bindless_multi_draw_indirect_count --------------- */
#ifndef GL_NV_bindless_multi_draw_indirect_count
#endif /* GL_NV_bindless_multi_draw_indirect_count */
/* ------------------------- GL_NV_bindless_texture ------------------------ */
#ifndef GL_NV_bindless_texture
#endif /* GL_NV_bindless_texture */
/* --------------------- GL_NV_blend_equation_advanced --------------------- */
#ifndef GL_NV_blend_equation_advanced
#endif /* GL_NV_blend_equation_advanced */
/* ----------------- GL_NV_blend_equation_advanced_coherent ---------------- */
#ifndef GL_NV_blend_equation_advanced_coherent
#endif /* GL_NV_blend_equation_advanced_coherent */
/* ----------------------- GL_NV_blend_minmax_factor ----------------------- */
#ifndef GL_NV_blend_minmax_factor
#endif /* GL_NV_blend_minmax_factor */
/* --------------------------- GL_NV_blend_square -------------------------- */
#ifndef GL_NV_blend_square
#endif /* GL_NV_blend_square */
/* ----------------------- GL_NV_clip_space_w_scaling ---------------------- */
#ifndef GL_NV_clip_space_w_scaling
#endif /* GL_NV_clip_space_w_scaling */
/* --------------------------- GL_NV_command_list -------------------------- */
#ifndef GL_NV_command_list
#endif /* GL_NV_command_list */
/* ------------------------- GL_NV_compute_program5 ------------------------ */
#ifndef GL_NV_compute_program5
#endif /* GL_NV_compute_program5 */
/* ------------------------ GL_NV_conditional_render ----------------------- */
#ifndef GL_NV_conditional_render
#endif /* GL_NV_conditional_render */
/* ----------------------- GL_NV_conservative_raster ----------------------- */
#ifndef GL_NV_conservative_raster
#endif /* GL_NV_conservative_raster */
/* -------------------- GL_NV_conservative_raster_dilate ------------------- */
#ifndef GL_NV_conservative_raster_dilate
#endif /* GL_NV_conservative_raster_dilate */
/* -------------- GL_NV_conservative_raster_pre_snap_triangles ------------- */
#ifndef GL_NV_conservative_raster_pre_snap_triangles
#endif /* GL_NV_conservative_raster_pre_snap_triangles */
/* --------------------------- GL_NV_copy_buffer --------------------------- */
#ifndef GL_NV_copy_buffer
#endif /* GL_NV_copy_buffer */
/* ----------------------- GL_NV_copy_depth_to_color ----------------------- */
#ifndef GL_NV_copy_depth_to_color
#endif /* GL_NV_copy_depth_to_color */
/* ---------------------------- GL_NV_copy_image --------------------------- */
#ifndef GL_NV_copy_image
#endif /* GL_NV_copy_image */
/* -------------------------- GL_NV_deep_texture3D ------------------------- */
#ifndef GL_NV_deep_texture3D
#endif /* GL_NV_deep_texture3D */
/* ------------------------ GL_NV_depth_buffer_float ----------------------- */
#ifndef GL_NV_depth_buffer_float
#endif /* GL_NV_depth_buffer_float */
/* --------------------------- GL_NV_depth_clamp --------------------------- */
#ifndef GL_NV_depth_clamp
#endif /* GL_NV_depth_clamp */
/* ---------------------- GL_NV_depth_range_unclamped ---------------------- */
#ifndef GL_NV_depth_range_unclamped
#endif /* GL_NV_depth_range_unclamped */
/* --------------------------- GL_NV_draw_buffers -------------------------- */
#ifndef GL_NV_draw_buffers
#endif /* GL_NV_draw_buffers */
/* -------------------------- GL_NV_draw_instanced ------------------------- */
#ifndef GL_NV_draw_instanced
#endif /* GL_NV_draw_instanced */
/* --------------------------- GL_NV_draw_texture -------------------------- */
#ifndef GL_NV_draw_texture
#endif /* GL_NV_draw_texture */
/* ------------------------ GL_NV_draw_vulkan_image ------------------------ */
#ifndef GL_NV_draw_vulkan_image
#endif /* GL_NV_draw_vulkan_image */
/* ---------------------------- GL_NV_evaluators --------------------------- */
#ifndef GL_NV_evaluators
#endif /* GL_NV_evaluators */
/* --------------------- GL_NV_explicit_attrib_location -------------------- */
#ifndef GL_NV_explicit_attrib_location
#endif /* GL_NV_explicit_attrib_location */
/* ----------------------- GL_NV_explicit_multisample ---------------------- */
#ifndef GL_NV_explicit_multisample
#endif /* GL_NV_explicit_multisample */
/* ---------------------- GL_NV_fbo_color_attachments ---------------------- */
#ifndef GL_NV_fbo_color_attachments
#endif /* GL_NV_fbo_color_attachments */
/* ------------------------------ GL_NV_fence ------------------------------ */
#ifndef GL_NV_fence
#endif /* GL_NV_fence */
/* -------------------------- GL_NV_fill_rectangle ------------------------- */
#ifndef GL_NV_fill_rectangle
#endif /* GL_NV_fill_rectangle */
/* --------------------------- GL_NV_float_buffer -------------------------- */
#ifndef GL_NV_float_buffer
#endif /* GL_NV_float_buffer */
/* --------------------------- GL_NV_fog_distance -------------------------- */
#ifndef GL_NV_fog_distance
#endif /* GL_NV_fog_distance */
/* -------------------- GL_NV_fragment_coverage_to_color ------------------- */
#ifndef GL_NV_fragment_coverage_to_color
#endif /* GL_NV_fragment_coverage_to_color */
/* ------------------------- GL_NV_fragment_program ------------------------ */
#ifndef GL_NV_fragment_program
#endif /* GL_NV_fragment_program */
/* ------------------------ GL_NV_fragment_program2 ------------------------ */
#ifndef GL_NV_fragment_program2
#endif /* GL_NV_fragment_program2 */
/* ------------------------ GL_NV_fragment_program4 ------------------------ */
#ifndef GL_NV_fragment_program4
#endif /* GL_NV_fragment_program4 */
/* --------------------- GL_NV_fragment_program_option --------------------- */
#ifndef GL_NV_fragment_program_option
#endif /* GL_NV_fragment_program_option */
/* -------------------- GL_NV_fragment_shader_interlock -------------------- */
#ifndef GL_NV_fragment_shader_interlock
#endif /* GL_NV_fragment_shader_interlock */
/* ------------------------- GL_NV_framebuffer_blit ------------------------ */
#ifndef GL_NV_framebuffer_blit
#endif /* GL_NV_framebuffer_blit */
/* -------------------- GL_NV_framebuffer_mixed_samples -------------------- */
#ifndef GL_NV_framebuffer_mixed_samples
#endif /* GL_NV_framebuffer_mixed_samples */
/* --------------------- GL_NV_framebuffer_multisample --------------------- */
#ifndef GL_NV_framebuffer_multisample
#endif /* GL_NV_framebuffer_multisample */
/* ----------------- GL_NV_framebuffer_multisample_coverage ---------------- */
#ifndef GL_NV_framebuffer_multisample_coverage
#endif /* GL_NV_framebuffer_multisample_coverage */
/* ----------------------- GL_NV_generate_mipmap_sRGB ---------------------- */
#ifndef GL_NV_generate_mipmap_sRGB
#endif /* GL_NV_generate_mipmap_sRGB */
/* ------------------------ GL_NV_geometry_program4 ------------------------ */
#ifndef GL_NV_geometry_program4
#endif /* GL_NV_geometry_program4 */
/* ------------------------- GL_NV_geometry_shader4 ------------------------ */
#ifndef GL_NV_geometry_shader4
#endif /* GL_NV_geometry_shader4 */
/* ------------------- GL_NV_geometry_shader_passthrough ------------------- */
#ifndef GL_NV_geometry_shader_passthrough
#endif /* GL_NV_geometry_shader_passthrough */
/* -------------------------- GL_NV_gpu_multicast -------------------------- */
#ifndef GL_NV_gpu_multicast
#endif /* GL_NV_gpu_multicast */
/* --------------------------- GL_NV_gpu_program4 -------------------------- */
#ifndef GL_NV_gpu_program4
#endif /* GL_NV_gpu_program4 */
/* --------------------------- GL_NV_gpu_program5 -------------------------- */
#ifndef GL_NV_gpu_program5
#endif /* GL_NV_gpu_program5 */
/* -------------------- GL_NV_gpu_program5_mem_extended -------------------- */
#ifndef GL_NV_gpu_program5_mem_extended
#endif /* GL_NV_gpu_program5_mem_extended */
/* ------------------------- GL_NV_gpu_program_fp64 ------------------------ */
#ifndef GL_NV_gpu_program_fp64
#endif /* GL_NV_gpu_program_fp64 */
/* --------------------------- GL_NV_gpu_shader5 --------------------------- */
#ifndef GL_NV_gpu_shader5
#endif /* GL_NV_gpu_shader5 */
/* ---------------------------- GL_NV_half_float --------------------------- */
#ifndef GL_NV_half_float
typedef unsigned short GLhalf;
#endif /* GL_NV_half_float */
/* -------------------------- GL_NV_image_formats -------------------------- */
#ifndef GL_NV_image_formats
#endif /* GL_NV_image_formats */
/* ------------------------- GL_NV_instanced_arrays ------------------------ */
#ifndef GL_NV_instanced_arrays
#endif /* GL_NV_instanced_arrays */
/* ------------------- GL_NV_internalformat_sample_query ------------------- */
#ifndef GL_NV_internalformat_sample_query
#endif /* GL_NV_internalformat_sample_query */
/* ------------------------ GL_NV_light_max_exponent ----------------------- */
#ifndef GL_NV_light_max_exponent
#endif /* GL_NV_light_max_exponent */
/* ----------------------- GL_NV_multisample_coverage ---------------------- */
#ifndef GL_NV_multisample_coverage
#endif /* GL_NV_multisample_coverage */
/* --------------------- GL_NV_multisample_filter_hint --------------------- */
#ifndef GL_NV_multisample_filter_hint
#endif /* GL_NV_multisample_filter_hint */
/* ----------------------- GL_NV_non_square_matrices ----------------------- */
#ifndef GL_NV_non_square_matrices
#endif /* GL_NV_non_square_matrices */
/* ------------------------- GL_NV_occlusion_query ------------------------- */
#ifndef GL_NV_occlusion_query
#endif /* GL_NV_occlusion_query */
/* -------------------------- GL_NV_pack_subimage -------------------------- */
#ifndef GL_NV_pack_subimage
#endif /* GL_NV_pack_subimage */
/* ----------------------- GL_NV_packed_depth_stencil ---------------------- */
#ifndef GL_NV_packed_depth_stencil
#endif /* GL_NV_packed_depth_stencil */
/* --------------------------- GL_NV_packed_float -------------------------- */
#ifndef GL_NV_packed_float
#endif /* GL_NV_packed_float */
/* ----------------------- GL_NV_packed_float_linear ----------------------- */
#ifndef GL_NV_packed_float_linear
#endif /* GL_NV_packed_float_linear */
/* --------------------- GL_NV_parameter_buffer_object --------------------- */
#ifndef GL_NV_parameter_buffer_object
#endif /* GL_NV_parameter_buffer_object */
/* --------------------- GL_NV_parameter_buffer_object2 -------------------- */
#ifndef GL_NV_parameter_buffer_object2
#endif /* GL_NV_parameter_buffer_object2 */
/* -------------------------- GL_NV_path_rendering ------------------------- */
#ifndef GL_NV_path_rendering
#endif /* GL_NV_path_rendering */
/* -------------------- GL_NV_path_rendering_shared_edge ------------------- */
#ifndef GL_NV_path_rendering_shared_edge
#endif /* GL_NV_path_rendering_shared_edge */
/* ----------------------- GL_NV_pixel_buffer_object ----------------------- */
#ifndef GL_NV_pixel_buffer_object
#endif /* GL_NV_pixel_buffer_object */
/* ------------------------- GL_NV_pixel_data_range ------------------------ */
#ifndef GL_NV_pixel_data_range
#endif /* GL_NV_pixel_data_range */
/* ------------------------- GL_NV_platform_binary ------------------------- */
#ifndef GL_NV_platform_binary
#endif /* GL_NV_platform_binary */
/* --------------------------- GL_NV_point_sprite -------------------------- */
#ifndef GL_NV_point_sprite
#endif /* GL_NV_point_sprite */
/* --------------------------- GL_NV_polygon_mode -------------------------- */
#ifndef GL_NV_polygon_mode
#endif /* GL_NV_polygon_mode */
/* -------------------------- GL_NV_present_video -------------------------- */
#ifndef GL_NV_present_video
#endif /* GL_NV_present_video */
/* ------------------------ GL_NV_primitive_restart ------------------------ */
#ifndef GL_NV_primitive_restart
#endif /* GL_NV_primitive_restart */
/* ---------------------------- GL_NV_read_depth --------------------------- */
#ifndef GL_NV_read_depth
#endif /* GL_NV_read_depth */
/* ------------------------ GL_NV_read_depth_stencil ----------------------- */
#ifndef GL_NV_read_depth_stencil
#endif /* GL_NV_read_depth_stencil */
/* --------------------------- GL_NV_read_stencil -------------------------- */
#ifndef GL_NV_read_stencil
#endif /* GL_NV_read_stencil */
/* ------------------------ GL_NV_register_combiners ----------------------- */
#ifndef GL_NV_register_combiners
#endif /* GL_NV_register_combiners */
/* ----------------------- GL_NV_register_combiners2 ----------------------- */
#ifndef GL_NV_register_combiners2
#endif /* GL_NV_register_combiners2 */
/* ------------------ GL_NV_robustness_video_memory_purge ------------------ */
#ifndef GL_NV_robustness_video_memory_purge
#endif /* GL_NV_robustness_video_memory_purge */
/* --------------------------- GL_NV_sRGB_formats -------------------------- */
#ifndef GL_NV_sRGB_formats
#endif /* GL_NV_sRGB_formats */
/* ------------------------- GL_NV_sample_locations ------------------------ */
#ifndef GL_NV_sample_locations
#endif /* GL_NV_sample_locations */
/* ------------------ GL_NV_sample_mask_override_coverage ------------------ */
#ifndef GL_NV_sample_mask_override_coverage
#endif /* GL_NV_sample_mask_override_coverage */
/* ---------------------- GL_NV_shader_atomic_counters --------------------- */
#ifndef GL_NV_shader_atomic_counters
#endif /* GL_NV_shader_atomic_counters */
/* ----------------------- GL_NV_shader_atomic_float ----------------------- */
#ifndef GL_NV_shader_atomic_float
#endif /* GL_NV_shader_atomic_float */
/* ---------------------- GL_NV_shader_atomic_float64 ---------------------- */
#ifndef GL_NV_shader_atomic_float64
#endif /* GL_NV_shader_atomic_float64 */
/* -------------------- GL_NV_shader_atomic_fp16_vector -------------------- */
#ifndef GL_NV_shader_atomic_fp16_vector
#endif /* GL_NV_shader_atomic_fp16_vector */
/* ----------------------- GL_NV_shader_atomic_int64 ----------------------- */
#ifndef GL_NV_shader_atomic_int64
#endif /* GL_NV_shader_atomic_int64 */
/* ------------------------ GL_NV_shader_buffer_load ----------------------- */
#ifndef GL_NV_shader_buffer_load
#endif /* GL_NV_shader_buffer_load */
/* ---------------- GL_NV_shader_noperspective_interpolation --------------- */
#ifndef GL_NV_shader_noperspective_interpolation
#endif /* GL_NV_shader_noperspective_interpolation */
/* ------------------- GL_NV_shader_storage_buffer_object ------------------ */
#ifndef GL_NV_shader_storage_buffer_object
#endif /* GL_NV_shader_storage_buffer_object */
/* ----------------------- GL_NV_shader_thread_group ----------------------- */
#ifndef GL_NV_shader_thread_group
#endif /* GL_NV_shader_thread_group */
/* ---------------------- GL_NV_shader_thread_shuffle ---------------------- */
#ifndef GL_NV_shader_thread_shuffle
#endif /* GL_NV_shader_thread_shuffle */
/* ---------------------- GL_NV_shadow_samplers_array ---------------------- */
#ifndef GL_NV_shadow_samplers_array
#endif /* GL_NV_shadow_samplers_array */
/* ----------------------- GL_NV_shadow_samplers_cube ---------------------- */
#ifndef GL_NV_shadow_samplers_cube
#endif /* GL_NV_shadow_samplers_cube */
/* ---------------------- GL_NV_stereo_view_rendering ---------------------- */
#ifndef GL_NV_stereo_view_rendering
#endif /* GL_NV_stereo_view_rendering */
/* ---------------------- GL_NV_tessellation_program5 ---------------------- */
#ifndef GL_NV_tessellation_program5
#endif /* GL_NV_tessellation_program5 */
/* -------------------------- GL_NV_texgen_emboss -------------------------- */
#ifndef GL_NV_texgen_emboss
#endif /* GL_NV_texgen_emboss */
/* ------------------------ GL_NV_texgen_reflection ------------------------ */
#ifndef GL_NV_texgen_reflection
#endif /* GL_NV_texgen_reflection */
/* -------------------------- GL_NV_texture_array -------------------------- */
#ifndef GL_NV_texture_array
#endif /* GL_NV_texture_array */
/* ------------------------- GL_NV_texture_barrier ------------------------- */
#ifndef GL_NV_texture_barrier
#endif /* GL_NV_texture_barrier */
/* ----------------------- GL_NV_texture_border_clamp ---------------------- */
#ifndef GL_NV_texture_border_clamp
#endif /* GL_NV_texture_border_clamp */
/* --------------------- GL_NV_texture_compression_latc -------------------- */
#ifndef GL_NV_texture_compression_latc
#endif /* GL_NV_texture_compression_latc */
/* --------------------- GL_NV_texture_compression_s3tc -------------------- */
#ifndef GL_NV_texture_compression_s3tc
#endif /* GL_NV_texture_compression_s3tc */
/* ----------------- GL_NV_texture_compression_s3tc_update ----------------- */
#ifndef GL_NV_texture_compression_s3tc_update
#endif /* GL_NV_texture_compression_s3tc_update */
/* --------------------- GL_NV_texture_compression_vtc --------------------- */
#ifndef GL_NV_texture_compression_vtc
#endif /* GL_NV_texture_compression_vtc */
/* ----------------------- GL_NV_texture_env_combine4 ---------------------- */
#ifndef GL_NV_texture_env_combine4
#endif /* GL_NV_texture_env_combine4 */
/* ---------------------- GL_NV_texture_expand_normal ---------------------- */
#ifndef GL_NV_texture_expand_normal
#endif /* GL_NV_texture_expand_normal */
/* ----------------------- GL_NV_texture_multisample ----------------------- */
#ifndef GL_NV_texture_multisample
#endif /* GL_NV_texture_multisample */
/* ---------------------- GL_NV_texture_npot_2D_mipmap --------------------- */
#ifndef GL_NV_texture_npot_2D_mipmap
#endif /* GL_NV_texture_npot_2D_mipmap */
/* ------------------------ GL_NV_texture_rectangle ------------------------ */
#ifndef GL_NV_texture_rectangle
#endif /* GL_NV_texture_rectangle */
/* ------------------- GL_NV_texture_rectangle_compressed ------------------ */
#ifndef GL_NV_texture_rectangle_compressed
#endif /* GL_NV_texture_rectangle_compressed */
/* -------------------------- GL_NV_texture_shader ------------------------- */
#ifndef GL_NV_texture_shader
#endif /* GL_NV_texture_shader */
/* ------------------------- GL_NV_texture_shader2 ------------------------- */
#ifndef GL_NV_texture_shader2
#endif /* GL_NV_texture_shader2 */
/* ------------------------- GL_NV_texture_shader3 ------------------------- */
#ifndef GL_NV_texture_shader3
#endif /* GL_NV_texture_shader3 */
/* ------------------------ GL_NV_transform_feedback ----------------------- */
#ifndef GL_NV_transform_feedback
#endif /* GL_NV_transform_feedback */
/* ----------------------- GL_NV_transform_feedback2 ----------------------- */
#ifndef GL_NV_transform_feedback2
#endif /* GL_NV_transform_feedback2 */
/* ------------------ GL_NV_uniform_buffer_unified_memory ------------------ */
#ifndef GL_NV_uniform_buffer_unified_memory
#endif /* GL_NV_uniform_buffer_unified_memory */
/* -------------------------- GL_NV_vdpau_interop -------------------------- */
#ifndef GL_NV_vdpau_interop
typedef GLintptr GLvdpauSurfaceNV;
#endif /* GL_NV_vdpau_interop */
/* ------------------------ GL_NV_vertex_array_range ----------------------- */
#ifndef GL_NV_vertex_array_range
#endif /* GL_NV_vertex_array_range */
/* ----------------------- GL_NV_vertex_array_range2 ----------------------- */
#ifndef GL_NV_vertex_array_range2
#endif /* GL_NV_vertex_array_range2 */
/* ------------------- GL_NV_vertex_attrib_integer_64bit ------------------- */
#ifndef GL_NV_vertex_attrib_integer_64bit
#endif /* GL_NV_vertex_attrib_integer_64bit */
/* ------------------- GL_NV_vertex_buffer_unified_memory ------------------ */
#ifndef GL_NV_vertex_buffer_unified_memory
#endif /* GL_NV_vertex_buffer_unified_memory */
/* -------------------------- GL_NV_vertex_program ------------------------- */
#ifndef GL_NV_vertex_program
#endif /* GL_NV_vertex_program */
/* ------------------------ GL_NV_vertex_program1_1 ------------------------ */
#ifndef GL_NV_vertex_program1_1
#endif /* GL_NV_vertex_program1_1 */
/* ------------------------- GL_NV_vertex_program2 ------------------------- */
#ifndef GL_NV_vertex_program2
#endif /* GL_NV_vertex_program2 */
/* ---------------------- GL_NV_vertex_program2_option --------------------- */
#ifndef GL_NV_vertex_program2_option
#endif /* GL_NV_vertex_program2_option */
/* ------------------------- GL_NV_vertex_program3 ------------------------- */
#ifndef GL_NV_vertex_program3
#endif /* GL_NV_vertex_program3 */
/* ------------------------- GL_NV_vertex_program4 ------------------------- */
#ifndef GL_NV_vertex_program4
#endif /* GL_NV_vertex_program4 */
/* -------------------------- GL_NV_video_capture -------------------------- */
#ifndef GL_NV_video_capture
#endif /* GL_NV_video_capture */
/* -------------------------- GL_NV_viewport_array ------------------------- */
#ifndef GL_NV_viewport_array
#endif /* GL_NV_viewport_array */
/* ------------------------- GL_NV_viewport_array2 ------------------------- */
#ifndef GL_NV_viewport_array2
#endif /* GL_NV_viewport_array2 */
/* ------------------------- GL_NV_viewport_swizzle ------------------------ */
#ifndef GL_NV_viewport_swizzle
#endif /* GL_NV_viewport_swizzle */
/* ------------------------ GL_OES_byte_coordinates ------------------------ */
#ifndef GL_OES_byte_coordinates
#endif /* GL_OES_byte_coordinates */
/* ---------------------------- GL_OML_interlace --------------------------- */
#ifndef GL_OML_interlace
#endif /* GL_OML_interlace */
/* ---------------------------- GL_OML_resample ---------------------------- */
#ifndef GL_OML_resample
#endif /* GL_OML_resample */
/* ---------------------------- GL_OML_subsample --------------------------- */
#ifndef GL_OML_subsample
#endif /* GL_OML_subsample */
/* ---------------------------- GL_OVR_multiview --------------------------- */
#ifndef GL_OVR_multiview
#endif /* GL_OVR_multiview */
/* --------------------------- GL_OVR_multiview2 --------------------------- */
#ifndef GL_OVR_multiview2
#endif /* GL_OVR_multiview2 */
/* ------------ GL_OVR_multiview_multisampled_render_to_texture ------------ */
#ifndef GL_OVR_multiview_multisampled_render_to_texture
#endif /* GL_OVR_multiview_multisampled_render_to_texture */
/* --------------------------- GL_PGI_misc_hints --------------------------- */
#ifndef GL_PGI_misc_hints
#endif /* GL_PGI_misc_hints */
/* -------------------------- GL_PGI_vertex_hints -------------------------- */
#ifndef GL_PGI_vertex_hints
#endif /* GL_PGI_vertex_hints */
/* --------------------------- GL_QCOM_alpha_test -------------------------- */
#ifndef GL_QCOM_alpha_test
#endif /* GL_QCOM_alpha_test */
/* ------------------------ GL_QCOM_binning_control ------------------------ */
#ifndef GL_QCOM_binning_control
#endif /* GL_QCOM_binning_control */
/* ------------------------- GL_QCOM_driver_control ------------------------ */
#ifndef GL_QCOM_driver_control
#endif /* GL_QCOM_driver_control */
/* -------------------------- GL_QCOM_extended_get ------------------------- */
#ifndef GL_QCOM_extended_get
#endif /* GL_QCOM_extended_get */
/* ------------------------- GL_QCOM_extended_get2 ------------------------- */
#ifndef GL_QCOM_extended_get2
#endif /* GL_QCOM_extended_get2 */
/* ---------------------- GL_QCOM_framebuffer_foveated --------------------- */
#ifndef GL_QCOM_framebuffer_foveated
#endif /* GL_QCOM_framebuffer_foveated */
/* ---------------------- GL_QCOM_perfmon_global_mode ---------------------- */
#ifndef GL_QCOM_perfmon_global_mode
#endif /* GL_QCOM_perfmon_global_mode */
/* -------------- GL_QCOM_shader_framebuffer_fetch_noncoherent ------------- */
#ifndef GL_QCOM_shader_framebuffer_fetch_noncoherent
#endif /* GL_QCOM_shader_framebuffer_fetch_noncoherent */
/* ------------------------ GL_QCOM_tiled_rendering ------------------------ */
#ifndef GL_QCOM_tiled_rendering
#endif /* GL_QCOM_tiled_rendering */
/* ---------------------- GL_QCOM_writeonly_rendering ---------------------- */
#ifndef GL_QCOM_writeonly_rendering
#endif /* GL_QCOM_writeonly_rendering */
/* ---------------------- GL_REGAL_ES1_0_compatibility --------------------- */
#ifndef GL_REGAL_ES1_0_compatibility
typedef int GLclampx;
#endif /* GL_REGAL_ES1_0_compatibility */
/* ---------------------- GL_REGAL_ES1_1_compatibility --------------------- */
#ifndef GL_REGAL_ES1_1_compatibility
#endif /* GL_REGAL_ES1_1_compatibility */
/* ---------------------------- GL_REGAL_enable ---------------------------- */
#ifndef GL_REGAL_enable
#endif /* GL_REGAL_enable */
/* ------------------------- GL_REGAL_error_string ------------------------- */
#ifndef GL_REGAL_error_string
#endif /* GL_REGAL_error_string */
/* ------------------------ GL_REGAL_extension_query ----------------------- */
#ifndef GL_REGAL_extension_query
#endif /* GL_REGAL_extension_query */
/* ------------------------------ GL_REGAL_log ----------------------------- */
#ifndef GL_REGAL_log
#endif /* GL_REGAL_log */
/* ------------------------- GL_REGAL_proc_address ------------------------- */
#ifndef GL_REGAL_proc_address
#endif /* GL_REGAL_proc_address */
/* ----------------------- GL_REND_screen_coordinates ---------------------- */
#ifndef GL_REND_screen_coordinates
#endif /* GL_REND_screen_coordinates */
/* ------------------------------- GL_S3_s3tc ------------------------------ */
#ifndef GL_S3_s3tc
#endif /* GL_S3_s3tc */
/* ------------------------- GL_SGIS_clip_band_hint ------------------------ */
#ifndef GL_SGIS_clip_band_hint
#endif /* GL_SGIS_clip_band_hint */
/* -------------------------- GL_SGIS_color_range -------------------------- */
#ifndef GL_SGIS_color_range
#endif /* GL_SGIS_color_range */
/* ------------------------- GL_SGIS_detail_texture ------------------------ */
#ifndef GL_SGIS_detail_texture
#endif /* GL_SGIS_detail_texture */
/* -------------------------- GL_SGIS_fog_function ------------------------- */
#ifndef GL_SGIS_fog_function
#endif /* GL_SGIS_fog_function */
/* ------------------------ GL_SGIS_generate_mipmap ------------------------ */
#ifndef GL_SGIS_generate_mipmap
#endif /* GL_SGIS_generate_mipmap */
/* -------------------------- GL_SGIS_line_texgen -------------------------- */
#ifndef GL_SGIS_line_texgen
#endif /* GL_SGIS_line_texgen */
/* -------------------------- GL_SGIS_multisample -------------------------- */
#ifndef GL_SGIS_multisample
#endif /* GL_SGIS_multisample */
/* -------------------------- GL_SGIS_multitexture ------------------------- */
#ifndef GL_SGIS_multitexture
#endif /* GL_SGIS_multitexture */
/* ------------------------- GL_SGIS_pixel_texture ------------------------- */
#ifndef GL_SGIS_pixel_texture
#endif /* GL_SGIS_pixel_texture */
/* ----------------------- GL_SGIS_point_line_texgen ----------------------- */
#ifndef GL_SGIS_point_line_texgen
#endif /* GL_SGIS_point_line_texgen */
/* ----------------------- GL_SGIS_shared_multisample ---------------------- */
#ifndef GL_SGIS_shared_multisample
#endif /* GL_SGIS_shared_multisample */
/* ------------------------ GL_SGIS_sharpen_texture ------------------------ */
#ifndef GL_SGIS_sharpen_texture
#endif /* GL_SGIS_sharpen_texture */
/* --------------------------- GL_SGIS_texture4D --------------------------- */
#ifndef GL_SGIS_texture4D
#endif /* GL_SGIS_texture4D */
/* ---------------------- GL_SGIS_texture_border_clamp --------------------- */
#ifndef GL_SGIS_texture_border_clamp
#endif /* GL_SGIS_texture_border_clamp */
/* ----------------------- GL_SGIS_texture_edge_clamp ---------------------- */
#ifndef GL_SGIS_texture_edge_clamp
#endif /* GL_SGIS_texture_edge_clamp */
/* ------------------------ GL_SGIS_texture_filter4 ------------------------ */
#ifndef GL_SGIS_texture_filter4
#endif /* GL_SGIS_texture_filter4 */
/* -------------------------- GL_SGIS_texture_lod -------------------------- */
#ifndef GL_SGIS_texture_lod
#endif /* GL_SGIS_texture_lod */
/* ------------------------- GL_SGIS_texture_select ------------------------ */
#ifndef GL_SGIS_texture_select
#endif /* GL_SGIS_texture_select */
/* ----------------------------- GL_SGIX_async ----------------------------- */
#ifndef GL_SGIX_async
#endif /* GL_SGIX_async */
/* ------------------------ GL_SGIX_async_histogram ------------------------ */
#ifndef GL_SGIX_async_histogram
#endif /* GL_SGIX_async_histogram */
/* -------------------------- GL_SGIX_async_pixel -------------------------- */
#ifndef GL_SGIX_async_pixel
#endif /* GL_SGIX_async_pixel */
/* ----------------------- GL_SGIX_bali_g_instruments ---------------------- */
#ifndef GL_SGIX_bali_g_instruments
#endif /* GL_SGIX_bali_g_instruments */
/* ----------------------- GL_SGIX_bali_r_instruments ---------------------- */
#ifndef GL_SGIX_bali_r_instruments
#endif /* GL_SGIX_bali_r_instruments */
/* --------------------- GL_SGIX_bali_timer_instruments -------------------- */
#ifndef GL_SGIX_bali_timer_instruments
#endif /* GL_SGIX_bali_timer_instruments */
/* ----------------------- GL_SGIX_blend_alpha_minmax ---------------------- */
#ifndef GL_SGIX_blend_alpha_minmax
#endif /* GL_SGIX_blend_alpha_minmax */
/* --------------------------- GL_SGIX_blend_cadd -------------------------- */
#ifndef GL_SGIX_blend_cadd
#endif /* GL_SGIX_blend_cadd */
/* ------------------------ GL_SGIX_blend_cmultiply ------------------------ */
#ifndef GL_SGIX_blend_cmultiply
#endif /* GL_SGIX_blend_cmultiply */
/* --------------------- GL_SGIX_calligraphic_fragment --------------------- */
#ifndef GL_SGIX_calligraphic_fragment
#endif /* GL_SGIX_calligraphic_fragment */
/* ---------------------------- GL_SGIX_clipmap ---------------------------- */
#ifndef GL_SGIX_clipmap
#endif /* GL_SGIX_clipmap */
/* --------------------- GL_SGIX_color_matrix_accuracy --------------------- */
#ifndef GL_SGIX_color_matrix_accuracy
#endif /* GL_SGIX_color_matrix_accuracy */
/* --------------------- GL_SGIX_color_table_index_mode -------------------- */
#ifndef GL_SGIX_color_table_index_mode
#endif /* GL_SGIX_color_table_index_mode */
/* ------------------------- GL_SGIX_complex_polar ------------------------- */
#ifndef GL_SGIX_complex_polar
#endif /* GL_SGIX_complex_polar */
/* ---------------------- GL_SGIX_convolution_accuracy --------------------- */
#ifndef GL_SGIX_convolution_accuracy
#endif /* GL_SGIX_convolution_accuracy */
/* ---------------------------- GL_SGIX_cube_map --------------------------- */
#ifndef GL_SGIX_cube_map
#endif /* GL_SGIX_cube_map */
/* ------------------------ GL_SGIX_cylinder_texgen ------------------------ */
#ifndef GL_SGIX_cylinder_texgen
#endif /* GL_SGIX_cylinder_texgen */
/* ---------------------------- GL_SGIX_datapipe --------------------------- */
#ifndef GL_SGIX_datapipe
#endif /* GL_SGIX_datapipe */
/* --------------------------- GL_SGIX_decimation -------------------------- */
#ifndef GL_SGIX_decimation
#endif /* GL_SGIX_decimation */
/* --------------------- GL_SGIX_depth_pass_instrument --------------------- */
#ifndef GL_SGIX_depth_pass_instrument
#endif /* GL_SGIX_depth_pass_instrument */
/* ------------------------- GL_SGIX_depth_texture ------------------------- */
#ifndef GL_SGIX_depth_texture
#endif /* GL_SGIX_depth_texture */
/* ------------------------------ GL_SGIX_dvc ------------------------------ */
#ifndef GL_SGIX_dvc
#endif /* GL_SGIX_dvc */
/* -------------------------- GL_SGIX_flush_raster ------------------------- */
#ifndef GL_SGIX_flush_raster
#endif /* GL_SGIX_flush_raster */
/* --------------------------- GL_SGIX_fog_blend --------------------------- */
#ifndef GL_SGIX_fog_blend
#endif /* GL_SGIX_fog_blend */
/* ---------------------- GL_SGIX_fog_factor_to_alpha ---------------------- */
#ifndef GL_SGIX_fog_factor_to_alpha
#endif /* GL_SGIX_fog_factor_to_alpha */
/* --------------------------- GL_SGIX_fog_layers -------------------------- */
#ifndef GL_SGIX_fog_layers
#endif /* GL_SGIX_fog_layers */
/* --------------------------- GL_SGIX_fog_offset -------------------------- */
#ifndef GL_SGIX_fog_offset
#endif /* GL_SGIX_fog_offset */
/* --------------------------- GL_SGIX_fog_patchy -------------------------- */
#ifndef GL_SGIX_fog_patchy
#endif /* GL_SGIX_fog_patchy */
/* --------------------------- GL_SGIX_fog_scale --------------------------- */
#ifndef GL_SGIX_fog_scale
#endif /* GL_SGIX_fog_scale */
/* -------------------------- GL_SGIX_fog_texture -------------------------- */
#ifndef GL_SGIX_fog_texture
#endif /* GL_SGIX_fog_texture */
/* -------------------- GL_SGIX_fragment_lighting_space -------------------- */
#ifndef GL_SGIX_fragment_lighting_space
#endif /* GL_SGIX_fragment_lighting_space */
/* ------------------- GL_SGIX_fragment_specular_lighting ------------------ */
#ifndef GL_SGIX_fragment_specular_lighting
#endif /* GL_SGIX_fragment_specular_lighting */
/* ---------------------- GL_SGIX_fragments_instrument --------------------- */
#ifndef GL_SGIX_fragments_instrument
#endif /* GL_SGIX_fragments_instrument */
/* --------------------------- GL_SGIX_framezoom --------------------------- */
#ifndef GL_SGIX_framezoom
#endif /* GL_SGIX_framezoom */
/* -------------------------- GL_SGIX_icc_texture -------------------------- */
#ifndef GL_SGIX_icc_texture
#endif /* GL_SGIX_icc_texture */
/* ------------------------ GL_SGIX_igloo_interface ------------------------ */
#ifndef GL_SGIX_igloo_interface
#endif /* GL_SGIX_igloo_interface */
/* ----------------------- GL_SGIX_image_compression ----------------------- */
#ifndef GL_SGIX_image_compression
#endif /* GL_SGIX_image_compression */
/* ---------------------- GL_SGIX_impact_pixel_texture --------------------- */
#ifndef GL_SGIX_impact_pixel_texture
#endif /* GL_SGIX_impact_pixel_texture */
/* ------------------------ GL_SGIX_instrument_error ----------------------- */
#ifndef GL_SGIX_instrument_error
#endif /* GL_SGIX_instrument_error */
/* --------------------------- GL_SGIX_interlace --------------------------- */
#ifndef GL_SGIX_interlace
#endif /* GL_SGIX_interlace */
/* ------------------------- GL_SGIX_ir_instrument1 ------------------------ */
#ifndef GL_SGIX_ir_instrument1
#endif /* GL_SGIX_ir_instrument1 */
/* ----------------------- GL_SGIX_line_quality_hint ----------------------- */
#ifndef GL_SGIX_line_quality_hint
#endif /* GL_SGIX_line_quality_hint */
/* ------------------------- GL_SGIX_list_priority ------------------------- */
#ifndef GL_SGIX_list_priority
#endif /* GL_SGIX_list_priority */
/* ----------------------------- GL_SGIX_mpeg1 ----------------------------- */
#ifndef GL_SGIX_mpeg1
#endif /* GL_SGIX_mpeg1 */
/* ----------------------------- GL_SGIX_mpeg2 ----------------------------- */
#ifndef GL_SGIX_mpeg2
#endif /* GL_SGIX_mpeg2 */
/* ------------------ GL_SGIX_nonlinear_lighting_pervertex ----------------- */
#ifndef GL_SGIX_nonlinear_lighting_pervertex
#endif /* GL_SGIX_nonlinear_lighting_pervertex */
/* --------------------------- GL_SGIX_nurbs_eval -------------------------- */
#ifndef GL_SGIX_nurbs_eval
#endif /* GL_SGIX_nurbs_eval */
/* ---------------------- GL_SGIX_occlusion_instrument --------------------- */
#ifndef GL_SGIX_occlusion_instrument
#endif /* GL_SGIX_occlusion_instrument */
/* ------------------------- GL_SGIX_packed_6bytes ------------------------- */
#ifndef GL_SGIX_packed_6bytes
#endif /* GL_SGIX_packed_6bytes */
/* ------------------------- GL_SGIX_pixel_texture ------------------------- */
#ifndef GL_SGIX_pixel_texture
#endif /* GL_SGIX_pixel_texture */
/* ----------------------- GL_SGIX_pixel_texture_bits ---------------------- */
#ifndef GL_SGIX_pixel_texture_bits
#endif /* GL_SGIX_pixel_texture_bits */
/* ----------------------- GL_SGIX_pixel_texture_lod ----------------------- */
#ifndef GL_SGIX_pixel_texture_lod
#endif /* GL_SGIX_pixel_texture_lod */
/* -------------------------- GL_SGIX_pixel_tiles -------------------------- */
#ifndef GL_SGIX_pixel_tiles
#endif /* GL_SGIX_pixel_tiles */
/* ------------------------- GL_SGIX_polynomial_ffd ------------------------ */
#ifndef GL_SGIX_polynomial_ffd
#endif /* GL_SGIX_polynomial_ffd */
/* --------------------------- GL_SGIX_quad_mesh --------------------------- */
#ifndef GL_SGIX_quad_mesh
#endif /* GL_SGIX_quad_mesh */
/* ------------------------ GL_SGIX_reference_plane ------------------------ */
#ifndef GL_SGIX_reference_plane
#endif /* GL_SGIX_reference_plane */
/* ---------------------------- GL_SGIX_resample --------------------------- */
#ifndef GL_SGIX_resample
#endif /* GL_SGIX_resample */
/* ------------------------- GL_SGIX_scalebias_hint ------------------------ */
#ifndef GL_SGIX_scalebias_hint
#endif /* GL_SGIX_scalebias_hint */
/* ----------------------------- GL_SGIX_shadow ---------------------------- */
#ifndef GL_SGIX_shadow
#endif /* GL_SGIX_shadow */
/* ------------------------- GL_SGIX_shadow_ambient ------------------------ */
#ifndef GL_SGIX_shadow_ambient
#endif /* GL_SGIX_shadow_ambient */
/* ------------------------------ GL_SGIX_slim ----------------------------- */
#ifndef GL_SGIX_slim
#endif /* GL_SGIX_slim */
/* ------------------------ GL_SGIX_spotlight_cutoff ----------------------- */
#ifndef GL_SGIX_spotlight_cutoff
#endif /* GL_SGIX_spotlight_cutoff */
/* ----------------------------- GL_SGIX_sprite ---------------------------- */
#ifndef GL_SGIX_sprite
#endif /* GL_SGIX_sprite */
/* -------------------------- GL_SGIX_subdiv_patch ------------------------- */
#ifndef GL_SGIX_subdiv_patch
#endif /* GL_SGIX_subdiv_patch */
/* --------------------------- GL_SGIX_subsample --------------------------- */
#ifndef GL_SGIX_subsample
#endif /* GL_SGIX_subsample */
/* ----------------------- GL_SGIX_tag_sample_buffer ----------------------- */
#ifndef GL_SGIX_tag_sample_buffer
#endif /* GL_SGIX_tag_sample_buffer */
/* ------------------------ GL_SGIX_texture_add_env ------------------------ */
#ifndef GL_SGIX_texture_add_env
#endif /* GL_SGIX_texture_add_env */
/* -------------------- GL_SGIX_texture_coordinate_clamp ------------------- */
#ifndef GL_SGIX_texture_coordinate_clamp
#endif /* GL_SGIX_texture_coordinate_clamp */
/* ------------------------ GL_SGIX_texture_lod_bias ----------------------- */
#ifndef GL_SGIX_texture_lod_bias
#endif /* GL_SGIX_texture_lod_bias */
/* ------------------- GL_SGIX_texture_mipmap_anisotropic ------------------ */
#ifndef GL_SGIX_texture_mipmap_anisotropic
#endif /* GL_SGIX_texture_mipmap_anisotropic */
/* ---------------------- GL_SGIX_texture_multi_buffer --------------------- */
#ifndef GL_SGIX_texture_multi_buffer
#endif /* GL_SGIX_texture_multi_buffer */
/* ------------------------- GL_SGIX_texture_phase ------------------------- */
#ifndef GL_SGIX_texture_phase
#endif /* GL_SGIX_texture_phase */
/* ------------------------- GL_SGIX_texture_range ------------------------- */
#ifndef GL_SGIX_texture_range
#endif /* GL_SGIX_texture_range */
/* ----------------------- GL_SGIX_texture_scale_bias ---------------------- */
#ifndef GL_SGIX_texture_scale_bias
#endif /* GL_SGIX_texture_scale_bias */
/* ---------------------- GL_SGIX_texture_supersample ---------------------- */
#ifndef GL_SGIX_texture_supersample
#endif /* GL_SGIX_texture_supersample */
/* --------------------------- GL_SGIX_vector_ops -------------------------- */
#ifndef GL_SGIX_vector_ops
#endif /* GL_SGIX_vector_ops */
/* ---------------------- GL_SGIX_vertex_array_object ---------------------- */
#ifndef GL_SGIX_vertex_array_object
#endif /* GL_SGIX_vertex_array_object */
/* ------------------------- GL_SGIX_vertex_preclip ------------------------ */
#ifndef GL_SGIX_vertex_preclip
#endif /* GL_SGIX_vertex_preclip */
/* ---------------------- GL_SGIX_vertex_preclip_hint ---------------------- */
#ifndef GL_SGIX_vertex_preclip_hint
#endif /* GL_SGIX_vertex_preclip_hint */
/* ----------------------------- GL_SGIX_ycrcb ----------------------------- */
#ifndef GL_SGIX_ycrcb
#endif /* GL_SGIX_ycrcb */
/* ------------------------ GL_SGIX_ycrcb_subsample ------------------------ */
#ifndef GL_SGIX_ycrcb_subsample
#endif /* GL_SGIX_ycrcb_subsample */
/* ----------------------------- GL_SGIX_ycrcba ---------------------------- */
#ifndef GL_SGIX_ycrcba
#endif /* GL_SGIX_ycrcba */
/* -------------------------- GL_SGI_color_matrix -------------------------- */
#ifndef GL_SGI_color_matrix
#endif /* GL_SGI_color_matrix */
/* --------------------------- GL_SGI_color_table -------------------------- */
#ifndef GL_SGI_color_table
#endif /* GL_SGI_color_table */
/* ----------------------------- GL_SGI_complex ---------------------------- */
#ifndef GL_SGI_complex
#endif /* GL_SGI_complex */
/* -------------------------- GL_SGI_complex_type -------------------------- */
#ifndef GL_SGI_complex_type
#endif /* GL_SGI_complex_type */
/* ------------------------------- GL_SGI_fft ------------------------------ */
#ifndef GL_SGI_fft
#endif /* GL_SGI_fft */
/* ----------------------- GL_SGI_texture_color_table ---------------------- */
#ifndef GL_SGI_texture_color_table
#endif /* GL_SGI_texture_color_table */
/* ------------------------- GL_SUNX_constant_data ------------------------- */
#ifndef GL_SUNX_constant_data
#endif /* GL_SUNX_constant_data */
/* -------------------- GL_SUN_convolution_border_modes -------------------- */
#ifndef GL_SUN_convolution_border_modes
#endif /* GL_SUN_convolution_border_modes */
/* -------------------------- GL_SUN_global_alpha -------------------------- */
#ifndef GL_SUN_global_alpha
#endif /* GL_SUN_global_alpha */
/* --------------------------- GL_SUN_mesh_array --------------------------- */
#ifndef GL_SUN_mesh_array
#endif /* GL_SUN_mesh_array */
/* ------------------------ GL_SUN_read_video_pixels ----------------------- */
#ifndef GL_SUN_read_video_pixels
#endif /* GL_SUN_read_video_pixels */
/* --------------------------- GL_SUN_slice_accum -------------------------- */
#ifndef GL_SUN_slice_accum
#endif /* GL_SUN_slice_accum */
/* -------------------------- GL_SUN_triangle_list ------------------------- */
#ifndef GL_SUN_triangle_list
#endif /* GL_SUN_triangle_list */
/* ----------------------------- GL_SUN_vertex ----------------------------- */
#ifndef GL_SUN_vertex
#endif /* GL_SUN_vertex */
/* -------------------------- GL_WIN_phong_shading ------------------------- */
#ifndef GL_WIN_phong_shading
#endif /* GL_WIN_phong_shading */
/* ------------------------- GL_WIN_scene_markerXXX ------------------------ */
#ifndef GL_WIN_scene_markerXXX
#endif /* GL_WIN_scene_markerXXX */
/* -------------------------- GL_WIN_specular_fog -------------------------- */
#ifndef GL_WIN_specular_fog
#endif /* GL_WIN_specular_fog */
/* ---------------------------- GL_WIN_swap_hint --------------------------- */
#ifndef GL_WIN_swap_hint
#endif /* GL_WIN_swap_hint */
/* ------------------------------------------------------------------------- */
GLEW_VAR_EXPORT GLboolean __GLEW_VERSION_1_1;
GLEW_VAR_EXPORT GLboolean __GLEW_VERSION_1_2;
GLEW_VAR_EXPORT GLboolean __GLEW_VERSION_1_2_1;
GLEW_VAR_EXPORT GLboolean __GLEW_VERSION_1_3;
GLEW_VAR_EXPORT GLboolean __GLEW_VERSION_1_4;
GLEW_VAR_EXPORT GLboolean __GLEW_VERSION_1_5;
GLEW_VAR_EXPORT GLboolean __GLEW_VERSION_2_0;
GLEW_VAR_EXPORT GLboolean __GLEW_VERSION_2_1;
GLEW_VAR_EXPORT GLboolean __GLEW_VERSION_3_0;
GLEW_VAR_EXPORT GLboolean __GLEW_VERSION_3_1;
GLEW_VAR_EXPORT GLboolean __GLEW_VERSION_3_2;
GLEW_VAR_EXPORT GLboolean __GLEW_VERSION_3_3;
GLEW_VAR_EXPORT GLboolean __GLEW_VERSION_4_0;
GLEW_VAR_EXPORT GLboolean __GLEW_VERSION_4_1;
GLEW_VAR_EXPORT GLboolean __GLEW_VERSION_4_2;
GLEW_VAR_EXPORT GLboolean __GLEW_VERSION_4_3;
GLEW_VAR_EXPORT GLboolean __GLEW_VERSION_4_4;
GLEW_VAR_EXPORT GLboolean __GLEW_VERSION_4_5;
GLEW_VAR_EXPORT GLboolean __GLEW_VERSION_4_6;
GLEW_VAR_EXPORT GLboolean __GLEW_3DFX_multisample;
GLEW_VAR_EXPORT GLboolean __GLEW_3DFX_tbuffer;
GLEW_VAR_EXPORT GLboolean __GLEW_3DFX_texture_compression_FXT1;
GLEW_VAR_EXPORT GLboolean __GLEW_AMD_blend_minmax_factor;
GLEW_VAR_EXPORT GLboolean __GLEW_AMD_compressed_3DC_texture;
GLEW_VAR_EXPORT GLboolean __GLEW_AMD_compressed_ATC_texture;
GLEW_VAR_EXPORT GLboolean __GLEW_AMD_conservative_depth;
GLEW_VAR_EXPORT GLboolean __GLEW_AMD_debug_output;
GLEW_VAR_EXPORT GLboolean __GLEW_AMD_depth_clamp_separate;
GLEW_VAR_EXPORT GLboolean __GLEW_AMD_draw_buffers_blend;
GLEW_VAR_EXPORT GLboolean __GLEW_AMD_framebuffer_sample_positions;
GLEW_VAR_EXPORT GLboolean __GLEW_AMD_gcn_shader;
GLEW_VAR_EXPORT GLboolean __GLEW_AMD_gpu_shader_half_float;
GLEW_VAR_EXPORT GLboolean __GLEW_AMD_gpu_shader_int16;
GLEW_VAR_EXPORT GLboolean __GLEW_AMD_gpu_shader_int64;
GLEW_VAR_EXPORT GLboolean __GLEW_AMD_interleaved_elements;
GLEW_VAR_EXPORT GLboolean __GLEW_AMD_multi_draw_indirect;
GLEW_VAR_EXPORT GLboolean __GLEW_AMD_name_gen_delete;
GLEW_VAR_EXPORT GLboolean __GLEW_AMD_occlusion_query_event;
GLEW_VAR_EXPORT GLboolean __GLEW_AMD_performance_monitor;
GLEW_VAR_EXPORT GLboolean __GLEW_AMD_pinned_memory;
GLEW_VAR_EXPORT GLboolean __GLEW_AMD_program_binary_Z400;
GLEW_VAR_EXPORT GLboolean __GLEW_AMD_query_buffer_object;
GLEW_VAR_EXPORT GLboolean __GLEW_AMD_sample_positions;
GLEW_VAR_EXPORT GLboolean __GLEW_AMD_seamless_cubemap_per_texture;
GLEW_VAR_EXPORT GLboolean __GLEW_AMD_shader_atomic_counter_ops;
GLEW_VAR_EXPORT GLboolean __GLEW_AMD_shader_ballot;
GLEW_VAR_EXPORT GLboolean __GLEW_AMD_shader_explicit_vertex_parameter;
GLEW_VAR_EXPORT GLboolean __GLEW_AMD_shader_stencil_export;
GLEW_VAR_EXPORT GLboolean __GLEW_AMD_shader_stencil_value_export;
GLEW_VAR_EXPORT GLboolean __GLEW_AMD_shader_trinary_minmax;
GLEW_VAR_EXPORT GLboolean __GLEW_AMD_sparse_texture;
GLEW_VAR_EXPORT GLboolean __GLEW_AMD_stencil_operation_extended;
GLEW_VAR_EXPORT GLboolean __GLEW_AMD_texture_gather_bias_lod;
GLEW_VAR_EXPORT GLboolean __GLEW_AMD_texture_texture4;
GLEW_VAR_EXPORT GLboolean __GLEW_AMD_transform_feedback3_lines_triangles;
GLEW_VAR_EXPORT GLboolean __GLEW_AMD_transform_feedback4;
GLEW_VAR_EXPORT GLboolean __GLEW_AMD_vertex_shader_layer;
GLEW_VAR_EXPORT GLboolean __GLEW_AMD_vertex_shader_tessellator;
GLEW_VAR_EXPORT GLboolean __GLEW_AMD_vertex_shader_viewport_index;
GLEW_VAR_EXPORT GLboolean __GLEW_ANDROID_extension_pack_es31a;
GLEW_VAR_EXPORT GLboolean __GLEW_ANGLE_depth_texture;
GLEW_VAR_EXPORT GLboolean __GLEW_ANGLE_framebuffer_blit;
GLEW_VAR_EXPORT GLboolean __GLEW_ANGLE_framebuffer_multisample;
GLEW_VAR_EXPORT GLboolean __GLEW_ANGLE_instanced_arrays;
GLEW_VAR_EXPORT GLboolean __GLEW_ANGLE_pack_reverse_row_order;
GLEW_VAR_EXPORT GLboolean __GLEW_ANGLE_program_binary;
GLEW_VAR_EXPORT GLboolean __GLEW_ANGLE_texture_compression_dxt1;
GLEW_VAR_EXPORT GLboolean __GLEW_ANGLE_texture_compression_dxt3;
GLEW_VAR_EXPORT GLboolean __GLEW_ANGLE_texture_compression_dxt5;
GLEW_VAR_EXPORT GLboolean __GLEW_ANGLE_texture_usage;
GLEW_VAR_EXPORT GLboolean __GLEW_ANGLE_timer_query;
GLEW_VAR_EXPORT GLboolean __GLEW_ANGLE_translated_shader_source;
GLEW_VAR_EXPORT GLboolean __GLEW_APPLE_aux_depth_stencil;
GLEW_VAR_EXPORT GLboolean __GLEW_APPLE_client_storage;
GLEW_VAR_EXPORT GLboolean __GLEW_APPLE_clip_distance;
GLEW_VAR_EXPORT GLboolean __GLEW_APPLE_color_buffer_packed_float;
GLEW_VAR_EXPORT GLboolean __GLEW_APPLE_copy_texture_levels;
GLEW_VAR_EXPORT GLboolean __GLEW_APPLE_element_array;
GLEW_VAR_EXPORT GLboolean __GLEW_APPLE_fence;
GLEW_VAR_EXPORT GLboolean __GLEW_APPLE_float_pixels;
GLEW_VAR_EXPORT GLboolean __GLEW_APPLE_flush_buffer_range;
GLEW_VAR_EXPORT GLboolean __GLEW_APPLE_framebuffer_multisample;
GLEW_VAR_EXPORT GLboolean __GLEW_APPLE_object_purgeable;
GLEW_VAR_EXPORT GLboolean __GLEW_APPLE_pixel_buffer;
GLEW_VAR_EXPORT GLboolean __GLEW_APPLE_rgb_422;
GLEW_VAR_EXPORT GLboolean __GLEW_APPLE_row_bytes;
GLEW_VAR_EXPORT GLboolean __GLEW_APPLE_specular_vector;
GLEW_VAR_EXPORT GLboolean __GLEW_APPLE_sync;
GLEW_VAR_EXPORT GLboolean __GLEW_APPLE_texture_2D_limited_npot;
GLEW_VAR_EXPORT GLboolean __GLEW_APPLE_texture_format_BGRA8888;
GLEW_VAR_EXPORT GLboolean __GLEW_APPLE_texture_max_level;
GLEW_VAR_EXPORT GLboolean __GLEW_APPLE_texture_packed_float;
GLEW_VAR_EXPORT GLboolean __GLEW_APPLE_texture_range;
GLEW_VAR_EXPORT GLboolean __GLEW_APPLE_transform_hint;
GLEW_VAR_EXPORT GLboolean __GLEW_APPLE_vertex_array_object;
GLEW_VAR_EXPORT GLboolean __GLEW_APPLE_vertex_array_range;
GLEW_VAR_EXPORT GLboolean __GLEW_APPLE_vertex_program_evaluators;
GLEW_VAR_EXPORT GLboolean __GLEW_APPLE_ycbcr_422;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_ES2_compatibility;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_ES3_1_compatibility;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_ES3_2_compatibility;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_ES3_compatibility;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_arrays_of_arrays;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_base_instance;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_bindless_texture;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_blend_func_extended;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_buffer_storage;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_cl_event;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_clear_buffer_object;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_clear_texture;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_clip_control;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_color_buffer_float;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_compatibility;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_compressed_texture_pixel_storage;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_compute_shader;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_compute_variable_group_size;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_conditional_render_inverted;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_conservative_depth;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_copy_buffer;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_copy_image;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_cull_distance;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_debug_output;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_depth_buffer_float;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_depth_clamp;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_depth_texture;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_derivative_control;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_direct_state_access;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_draw_buffers;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_draw_buffers_blend;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_draw_elements_base_vertex;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_draw_indirect;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_draw_instanced;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_enhanced_layouts;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_explicit_attrib_location;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_explicit_uniform_location;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_fragment_coord_conventions;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_fragment_layer_viewport;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_fragment_program;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_fragment_program_shadow;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_fragment_shader;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_fragment_shader_interlock;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_framebuffer_no_attachments;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_framebuffer_object;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_framebuffer_sRGB;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_geometry_shader4;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_get_program_binary;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_get_texture_sub_image;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_gl_spirv;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_gpu_shader5;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_gpu_shader_fp64;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_gpu_shader_int64;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_half_float_pixel;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_half_float_vertex;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_imaging;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_indirect_parameters;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_instanced_arrays;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_internalformat_query;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_internalformat_query2;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_invalidate_subdata;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_map_buffer_alignment;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_map_buffer_range;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_matrix_palette;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_multi_bind;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_multi_draw_indirect;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_multisample;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_multitexture;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_occlusion_query;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_occlusion_query2;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_parallel_shader_compile;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_pipeline_statistics_query;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_pixel_buffer_object;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_point_parameters;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_point_sprite;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_polygon_offset_clamp;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_post_depth_coverage;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_program_interface_query;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_provoking_vertex;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_query_buffer_object;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_robust_buffer_access_behavior;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_robustness;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_robustness_application_isolation;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_robustness_share_group_isolation;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_sample_locations;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_sample_shading;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_sampler_objects;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_seamless_cube_map;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_seamless_cubemap_per_texture;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_separate_shader_objects;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_shader_atomic_counter_ops;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_shader_atomic_counters;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_shader_ballot;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_shader_bit_encoding;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_shader_clock;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_shader_draw_parameters;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_shader_group_vote;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_shader_image_load_store;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_shader_image_size;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_shader_objects;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_shader_precision;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_shader_stencil_export;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_shader_storage_buffer_object;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_shader_subroutine;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_shader_texture_image_samples;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_shader_texture_lod;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_shader_viewport_layer_array;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_shading_language_100;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_shading_language_420pack;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_shading_language_include;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_shading_language_packing;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_shadow;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_shadow_ambient;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_sparse_buffer;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_sparse_texture;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_sparse_texture2;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_sparse_texture_clamp;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_spirv_extensions;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_stencil_texturing;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_sync;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_tessellation_shader;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_texture_barrier;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_texture_border_clamp;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_texture_buffer_object;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_texture_buffer_object_rgb32;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_texture_buffer_range;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_texture_compression;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_texture_compression_bptc;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_texture_compression_rgtc;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_texture_cube_map;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_texture_cube_map_array;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_texture_env_add;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_texture_env_combine;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_texture_env_crossbar;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_texture_env_dot3;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_texture_filter_anisotropic;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_texture_filter_minmax;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_texture_float;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_texture_gather;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_texture_mirror_clamp_to_edge;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_texture_mirrored_repeat;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_texture_multisample;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_texture_non_power_of_two;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_texture_query_levels;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_texture_query_lod;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_texture_rectangle;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_texture_rg;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_texture_rgb10_a2ui;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_texture_stencil8;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_texture_storage;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_texture_storage_multisample;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_texture_swizzle;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_texture_view;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_timer_query;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_transform_feedback2;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_transform_feedback3;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_transform_feedback_instanced;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_transform_feedback_overflow_query;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_transpose_matrix;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_uniform_buffer_object;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_vertex_array_bgra;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_vertex_array_object;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_vertex_attrib_64bit;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_vertex_attrib_binding;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_vertex_blend;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_vertex_buffer_object;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_vertex_program;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_vertex_shader;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_vertex_type_10f_11f_11f_rev;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_vertex_type_2_10_10_10_rev;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_viewport_array;
GLEW_VAR_EXPORT GLboolean __GLEW_ARB_window_pos;
GLEW_VAR_EXPORT GLboolean __GLEW_ARM_mali_program_binary;
GLEW_VAR_EXPORT GLboolean __GLEW_ARM_mali_shader_binary;
GLEW_VAR_EXPORT GLboolean __GLEW_ARM_rgba8;
GLEW_VAR_EXPORT GLboolean __GLEW_ARM_shader_framebuffer_fetch;
GLEW_VAR_EXPORT GLboolean __GLEW_ARM_shader_framebuffer_fetch_depth_stencil;
GLEW_VAR_EXPORT GLboolean __GLEW_ATIX_point_sprites;
GLEW_VAR_EXPORT GLboolean __GLEW_ATIX_texture_env_combine3;
GLEW_VAR_EXPORT GLboolean __GLEW_ATIX_texture_env_route;
GLEW_VAR_EXPORT GLboolean __GLEW_ATIX_vertex_shader_output_point_size;
GLEW_VAR_EXPORT GLboolean __GLEW_ATI_draw_buffers;
GLEW_VAR_EXPORT GLboolean __GLEW_ATI_element_array;
GLEW_VAR_EXPORT GLboolean __GLEW_ATI_envmap_bumpmap;
GLEW_VAR_EXPORT GLboolean __GLEW_ATI_fragment_shader;
GLEW_VAR_EXPORT GLboolean __GLEW_ATI_map_object_buffer;
GLEW_VAR_EXPORT GLboolean __GLEW_ATI_meminfo;
GLEW_VAR_EXPORT GLboolean __GLEW_ATI_pn_triangles;
GLEW_VAR_EXPORT GLboolean __GLEW_ATI_separate_stencil;
GLEW_VAR_EXPORT GLboolean __GLEW_ATI_shader_texture_lod;
GLEW_VAR_EXPORT GLboolean __GLEW_ATI_text_fragment_shader;
GLEW_VAR_EXPORT GLboolean __GLEW_ATI_texture_compression_3dc;
GLEW_VAR_EXPORT GLboolean __GLEW_ATI_texture_env_combine3;
GLEW_VAR_EXPORT GLboolean __GLEW_ATI_texture_float;
GLEW_VAR_EXPORT GLboolean __GLEW_ATI_texture_mirror_once;
GLEW_VAR_EXPORT GLboolean __GLEW_ATI_vertex_array_object;
GLEW_VAR_EXPORT GLboolean __GLEW_ATI_vertex_attrib_array_object;
GLEW_VAR_EXPORT GLboolean __GLEW_ATI_vertex_streams;
GLEW_VAR_EXPORT GLboolean __GLEW_EGL_KHR_context_flush_control;
GLEW_VAR_EXPORT GLboolean __GLEW_EGL_NV_robustness_video_memory_purge;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_422_pixels;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_Cg_shader;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_EGL_image_array;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_YUV_target;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_abgr;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_base_instance;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_bgra;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_bindable_uniform;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_blend_color;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_blend_equation_separate;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_blend_func_extended;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_blend_func_separate;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_blend_logic_op;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_blend_minmax;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_blend_subtract;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_buffer_storage;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_clear_texture;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_clip_cull_distance;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_clip_volume_hint;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_cmyka;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_color_buffer_float;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_color_buffer_half_float;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_color_subtable;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_compiled_vertex_array;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_compressed_ETC1_RGB8_sub_texture;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_conservative_depth;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_convolution;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_coordinate_frame;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_copy_image;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_copy_texture;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_cull_vertex;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_debug_label;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_debug_marker;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_depth_bounds_test;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_direct_state_access;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_discard_framebuffer;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_draw_buffers;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_draw_buffers2;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_draw_buffers_indexed;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_draw_elements_base_vertex;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_draw_instanced;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_draw_range_elements;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_external_buffer;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_float_blend;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_fog_coord;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_frag_depth;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_fragment_lighting;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_framebuffer_blit;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_framebuffer_multisample;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_framebuffer_multisample_blit_scaled;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_framebuffer_object;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_framebuffer_sRGB;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_geometry_point_size;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_geometry_shader;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_geometry_shader4;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_gpu_program_parameters;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_gpu_shader4;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_gpu_shader5;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_histogram;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_index_array_formats;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_index_func;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_index_material;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_index_texture;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_instanced_arrays;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_light_texture;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_map_buffer_range;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_memory_object;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_memory_object_fd;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_memory_object_win32;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_misc_attribute;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_multi_draw_arrays;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_multi_draw_indirect;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_multiple_textures;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_multisample;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_multisample_compatibility;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_multisampled_render_to_texture;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_multisampled_render_to_texture2;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_multiview_draw_buffers;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_packed_depth_stencil;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_packed_float;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_packed_pixels;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_paletted_texture;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_pixel_buffer_object;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_pixel_transform;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_pixel_transform_color_table;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_point_parameters;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_polygon_offset;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_polygon_offset_clamp;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_post_depth_coverage;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_provoking_vertex;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_pvrtc_sRGB;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_raster_multisample;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_read_format_bgra;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_render_snorm;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_rescale_normal;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_sRGB;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_sRGB_write_control;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_scene_marker;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_secondary_color;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_semaphore;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_semaphore_fd;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_semaphore_win32;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_separate_shader_objects;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_separate_specular_color;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_shader_framebuffer_fetch;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_shader_group_vote;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_shader_image_load_formatted;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_shader_image_load_store;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_shader_implicit_conversions;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_shader_integer_mix;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_shader_io_blocks;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_shader_non_constant_global_initializers;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_shader_pixel_local_storage;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_shader_pixel_local_storage2;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_shader_texture_lod;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_shadow_funcs;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_shadow_samplers;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_shared_texture_palette;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_sparse_texture;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_sparse_texture2;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_stencil_clear_tag;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_stencil_two_side;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_stencil_wrap;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_subtexture;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_texture;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_texture3D;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_texture_array;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_texture_buffer_object;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_texture_compression_astc_decode_mode;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_texture_compression_astc_decode_mode_rgb9e5;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_texture_compression_bptc;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_texture_compression_dxt1;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_texture_compression_latc;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_texture_compression_rgtc;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_texture_compression_s3tc;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_texture_cube_map;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_texture_cube_map_array;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_texture_edge_clamp;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_texture_env;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_texture_env_add;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_texture_env_combine;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_texture_env_dot3;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_texture_filter_anisotropic;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_texture_filter_minmax;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_texture_format_BGRA8888;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_texture_integer;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_texture_lod_bias;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_texture_mirror_clamp;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_texture_norm16;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_texture_object;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_texture_perturb_normal;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_texture_rectangle;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_texture_rg;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_texture_sRGB;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_texture_sRGB_R8;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_texture_sRGB_RG8;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_texture_sRGB_decode;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_texture_shared_exponent;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_texture_snorm;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_texture_storage;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_texture_swizzle;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_texture_type_2_10_10_10_REV;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_texture_view;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_timer_query;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_transform_feedback;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_unpack_subimage;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_vertex_array;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_vertex_array_bgra;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_vertex_array_setXXX;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_vertex_attrib_64bit;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_vertex_shader;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_vertex_weighting;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_win32_keyed_mutex;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_window_rectangles;
GLEW_VAR_EXPORT GLboolean __GLEW_EXT_x11_sync_object;
GLEW_VAR_EXPORT GLboolean __GLEW_GREMEDY_frame_terminator;
GLEW_VAR_EXPORT GLboolean __GLEW_GREMEDY_string_marker;
GLEW_VAR_EXPORT GLboolean __GLEW_HP_convolution_border_modes;
GLEW_VAR_EXPORT GLboolean __GLEW_HP_image_transform;
GLEW_VAR_EXPORT GLboolean __GLEW_HP_occlusion_test;
GLEW_VAR_EXPORT GLboolean __GLEW_HP_texture_lighting;
GLEW_VAR_EXPORT GLboolean __GLEW_IBM_cull_vertex;
GLEW_VAR_EXPORT GLboolean __GLEW_IBM_multimode_draw_arrays;
GLEW_VAR_EXPORT GLboolean __GLEW_IBM_rasterpos_clip;
GLEW_VAR_EXPORT GLboolean __GLEW_IBM_static_data;
GLEW_VAR_EXPORT GLboolean __GLEW_IBM_texture_mirrored_repeat;
GLEW_VAR_EXPORT GLboolean __GLEW_IBM_vertex_array_lists;
GLEW_VAR_EXPORT GLboolean __GLEW_INGR_color_clamp;
GLEW_VAR_EXPORT GLboolean __GLEW_INGR_interlace_read;
GLEW_VAR_EXPORT GLboolean __GLEW_INTEL_conservative_rasterization;
GLEW_VAR_EXPORT GLboolean __GLEW_INTEL_fragment_shader_ordering;
GLEW_VAR_EXPORT GLboolean __GLEW_INTEL_framebuffer_CMAA;
GLEW_VAR_EXPORT GLboolean __GLEW_INTEL_map_texture;
GLEW_VAR_EXPORT GLboolean __GLEW_INTEL_parallel_arrays;
GLEW_VAR_EXPORT GLboolean __GLEW_INTEL_performance_query;
GLEW_VAR_EXPORT GLboolean __GLEW_INTEL_texture_scissor;
GLEW_VAR_EXPORT GLboolean __GLEW_KHR_blend_equation_advanced;
GLEW_VAR_EXPORT GLboolean __GLEW_KHR_blend_equation_advanced_coherent;
GLEW_VAR_EXPORT GLboolean __GLEW_KHR_context_flush_control;
GLEW_VAR_EXPORT GLboolean __GLEW_KHR_debug;
GLEW_VAR_EXPORT GLboolean __GLEW_KHR_no_error;
GLEW_VAR_EXPORT GLboolean __GLEW_KHR_parallel_shader_compile;
GLEW_VAR_EXPORT GLboolean __GLEW_KHR_robust_buffer_access_behavior;
GLEW_VAR_EXPORT GLboolean __GLEW_KHR_robustness;
GLEW_VAR_EXPORT GLboolean __GLEW_KHR_texture_compression_astc_hdr;
GLEW_VAR_EXPORT GLboolean __GLEW_KHR_texture_compression_astc_ldr;
GLEW_VAR_EXPORT GLboolean __GLEW_KHR_texture_compression_astc_sliced_3d;
GLEW_VAR_EXPORT GLboolean __GLEW_KTX_buffer_region;
GLEW_VAR_EXPORT GLboolean __GLEW_MESAX_texture_stack;
GLEW_VAR_EXPORT GLboolean __GLEW_MESA_pack_invert;
GLEW_VAR_EXPORT GLboolean __GLEW_MESA_resize_buffers;
GLEW_VAR_EXPORT GLboolean __GLEW_MESA_shader_integer_functions;
GLEW_VAR_EXPORT GLboolean __GLEW_MESA_window_pos;
GLEW_VAR_EXPORT GLboolean __GLEW_MESA_ycbcr_texture;
GLEW_VAR_EXPORT GLboolean __GLEW_NVX_blend_equation_advanced_multi_draw_buffers;
GLEW_VAR_EXPORT GLboolean __GLEW_NVX_conditional_render;
GLEW_VAR_EXPORT GLboolean __GLEW_NVX_gpu_memory_info;
GLEW_VAR_EXPORT GLboolean __GLEW_NVX_linked_gpu_multicast;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_3dvision_settings;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_EGL_stream_consumer_external;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_alpha_to_coverage_dither_control;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_bgr;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_bindless_multi_draw_indirect;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_bindless_multi_draw_indirect_count;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_bindless_texture;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_blend_equation_advanced;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_blend_equation_advanced_coherent;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_blend_minmax_factor;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_blend_square;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_clip_space_w_scaling;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_command_list;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_compute_program5;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_conditional_render;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_conservative_raster;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_conservative_raster_dilate;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_conservative_raster_pre_snap_triangles;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_copy_buffer;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_copy_depth_to_color;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_copy_image;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_deep_texture3D;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_depth_buffer_float;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_depth_clamp;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_depth_range_unclamped;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_draw_buffers;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_draw_instanced;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_draw_texture;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_draw_vulkan_image;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_evaluators;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_explicit_attrib_location;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_explicit_multisample;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_fbo_color_attachments;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_fence;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_fill_rectangle;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_float_buffer;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_fog_distance;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_fragment_coverage_to_color;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_fragment_program;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_fragment_program2;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_fragment_program4;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_fragment_program_option;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_fragment_shader_interlock;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_framebuffer_blit;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_framebuffer_mixed_samples;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_framebuffer_multisample;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_framebuffer_multisample_coverage;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_generate_mipmap_sRGB;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_geometry_program4;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_geometry_shader4;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_geometry_shader_passthrough;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_gpu_multicast;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_gpu_program4;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_gpu_program5;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_gpu_program5_mem_extended;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_gpu_program_fp64;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_gpu_shader5;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_half_float;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_image_formats;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_instanced_arrays;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_internalformat_sample_query;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_light_max_exponent;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_multisample_coverage;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_multisample_filter_hint;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_non_square_matrices;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_occlusion_query;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_pack_subimage;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_packed_depth_stencil;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_packed_float;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_packed_float_linear;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_parameter_buffer_object;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_parameter_buffer_object2;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_path_rendering;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_path_rendering_shared_edge;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_pixel_buffer_object;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_pixel_data_range;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_platform_binary;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_point_sprite;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_polygon_mode;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_present_video;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_primitive_restart;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_read_depth;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_read_depth_stencil;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_read_stencil;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_register_combiners;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_register_combiners2;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_robustness_video_memory_purge;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_sRGB_formats;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_sample_locations;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_sample_mask_override_coverage;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_shader_atomic_counters;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_shader_atomic_float;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_shader_atomic_float64;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_shader_atomic_fp16_vector;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_shader_atomic_int64;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_shader_buffer_load;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_shader_noperspective_interpolation;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_shader_storage_buffer_object;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_shader_thread_group;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_shader_thread_shuffle;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_shadow_samplers_array;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_shadow_samplers_cube;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_stereo_view_rendering;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_tessellation_program5;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_texgen_emboss;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_texgen_reflection;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_texture_array;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_texture_barrier;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_texture_border_clamp;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_texture_compression_latc;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_texture_compression_s3tc;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_texture_compression_s3tc_update;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_texture_compression_vtc;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_texture_env_combine4;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_texture_expand_normal;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_texture_multisample;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_texture_npot_2D_mipmap;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_texture_rectangle;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_texture_rectangle_compressed;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_texture_shader;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_texture_shader2;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_texture_shader3;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_transform_feedback;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_transform_feedback2;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_uniform_buffer_unified_memory;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_vdpau_interop;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_vertex_array_range;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_vertex_array_range2;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_vertex_attrib_integer_64bit;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_vertex_buffer_unified_memory;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_vertex_program;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_vertex_program1_1;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_vertex_program2;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_vertex_program2_option;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_vertex_program3;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_vertex_program4;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_video_capture;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_viewport_array;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_viewport_array2;
GLEW_VAR_EXPORT GLboolean __GLEW_NV_viewport_swizzle;
GLEW_VAR_EXPORT GLboolean __GLEW_OES_byte_coordinates;
GLEW_VAR_EXPORT GLboolean __GLEW_OML_interlace;
GLEW_VAR_EXPORT GLboolean __GLEW_OML_resample;
GLEW_VAR_EXPORT GLboolean __GLEW_OML_subsample;
GLEW_VAR_EXPORT GLboolean __GLEW_OVR_multiview;
GLEW_VAR_EXPORT GLboolean __GLEW_OVR_multiview2;
GLEW_VAR_EXPORT GLboolean __GLEW_OVR_multiview_multisampled_render_to_texture;
GLEW_VAR_EXPORT GLboolean __GLEW_PGI_misc_hints;
GLEW_VAR_EXPORT GLboolean __GLEW_PGI_vertex_hints;
GLEW_VAR_EXPORT GLboolean __GLEW_QCOM_alpha_test;
GLEW_VAR_EXPORT GLboolean __GLEW_QCOM_binning_control;
GLEW_VAR_EXPORT GLboolean __GLEW_QCOM_driver_control;
GLEW_VAR_EXPORT GLboolean __GLEW_QCOM_extended_get;
GLEW_VAR_EXPORT GLboolean __GLEW_QCOM_extended_get2;
GLEW_VAR_EXPORT GLboolean __GLEW_QCOM_framebuffer_foveated;
GLEW_VAR_EXPORT GLboolean __GLEW_QCOM_perfmon_global_mode;
GLEW_VAR_EXPORT GLboolean __GLEW_QCOM_shader_framebuffer_fetch_noncoherent;
GLEW_VAR_EXPORT GLboolean __GLEW_QCOM_tiled_rendering;
GLEW_VAR_EXPORT GLboolean __GLEW_QCOM_writeonly_rendering;
GLEW_VAR_EXPORT GLboolean __GLEW_REGAL_ES1_0_compatibility;
GLEW_VAR_EXPORT GLboolean __GLEW_REGAL_ES1_1_compatibility;
GLEW_VAR_EXPORT GLboolean __GLEW_REGAL_enable;
GLEW_VAR_EXPORT GLboolean __GLEW_REGAL_error_string;
GLEW_VAR_EXPORT GLboolean __GLEW_REGAL_extension_query;
GLEW_VAR_EXPORT GLboolean __GLEW_REGAL_log;
GLEW_VAR_EXPORT GLboolean __GLEW_REGAL_proc_address;
GLEW_VAR_EXPORT GLboolean __GLEW_REND_screen_coordinates;
GLEW_VAR_EXPORT GLboolean __GLEW_S3_s3tc;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIS_clip_band_hint;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIS_color_range;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIS_detail_texture;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIS_fog_function;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIS_generate_mipmap;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIS_line_texgen;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIS_multisample;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIS_multitexture;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIS_pixel_texture;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIS_point_line_texgen;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIS_shared_multisample;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIS_sharpen_texture;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIS_texture4D;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIS_texture_border_clamp;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIS_texture_edge_clamp;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIS_texture_filter4;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIS_texture_lod;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIS_texture_select;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_async;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_async_histogram;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_async_pixel;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_bali_g_instruments;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_bali_r_instruments;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_bali_timer_instruments;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_blend_alpha_minmax;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_blend_cadd;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_blend_cmultiply;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_calligraphic_fragment;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_clipmap;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_color_matrix_accuracy;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_color_table_index_mode;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_complex_polar;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_convolution_accuracy;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_cube_map;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_cylinder_texgen;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_datapipe;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_decimation;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_depth_pass_instrument;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_depth_texture;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_dvc;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_flush_raster;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_fog_blend;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_fog_factor_to_alpha;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_fog_layers;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_fog_offset;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_fog_patchy;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_fog_scale;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_fog_texture;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_fragment_lighting_space;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_fragment_specular_lighting;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_fragments_instrument;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_framezoom;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_icc_texture;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_igloo_interface;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_image_compression;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_impact_pixel_texture;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_instrument_error;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_interlace;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_ir_instrument1;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_line_quality_hint;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_list_priority;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_mpeg1;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_mpeg2;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_nonlinear_lighting_pervertex;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_nurbs_eval;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_occlusion_instrument;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_packed_6bytes;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_pixel_texture;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_pixel_texture_bits;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_pixel_texture_lod;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_pixel_tiles;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_polynomial_ffd;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_quad_mesh;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_reference_plane;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_resample;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_scalebias_hint;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_shadow;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_shadow_ambient;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_slim;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_spotlight_cutoff;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_sprite;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_subdiv_patch;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_subsample;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_tag_sample_buffer;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_texture_add_env;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_texture_coordinate_clamp;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_texture_lod_bias;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_texture_mipmap_anisotropic;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_texture_multi_buffer;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_texture_phase;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_texture_range;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_texture_scale_bias;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_texture_supersample;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_vector_ops;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_vertex_array_object;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_vertex_preclip;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_vertex_preclip_hint;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_ycrcb;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_ycrcb_subsample;
GLEW_VAR_EXPORT GLboolean __GLEW_SGIX_ycrcba;
GLEW_VAR_EXPORT GLboolean __GLEW_SGI_color_matrix;
GLEW_VAR_EXPORT GLboolean __GLEW_SGI_color_table;
GLEW_VAR_EXPORT GLboolean __GLEW_SGI_complex;
GLEW_VAR_EXPORT GLboolean __GLEW_SGI_complex_type;
GLEW_VAR_EXPORT GLboolean __GLEW_SGI_fft;
GLEW_VAR_EXPORT GLboolean __GLEW_SGI_texture_color_table;
GLEW_VAR_EXPORT GLboolean __GLEW_SUNX_constant_data;
GLEW_VAR_EXPORT GLboolean __GLEW_SUN_convolution_border_modes;
GLEW_VAR_EXPORT GLboolean __GLEW_SUN_global_alpha;
GLEW_VAR_EXPORT GLboolean __GLEW_SUN_mesh_array;
GLEW_VAR_EXPORT GLboolean __GLEW_SUN_read_video_pixels;
GLEW_VAR_EXPORT GLboolean __GLEW_SUN_slice_accum;
GLEW_VAR_EXPORT GLboolean __GLEW_SUN_triangle_list;
GLEW_VAR_EXPORT GLboolean __GLEW_SUN_vertex;
GLEW_VAR_EXPORT GLboolean __GLEW_WIN_phong_shading;
GLEW_VAR_EXPORT GLboolean __GLEW_WIN_scene_markerXXX;
GLEW_VAR_EXPORT GLboolean __GLEW_WIN_specular_fog;
GLEW_VAR_EXPORT GLboolean __GLEW_WIN_swap_hint;
/* ------------------------------------------------------------------------- */
/* error codes */
/* string codes */
/* ------------------------------------------------------------------------- */
/* GLEW version info */
/*
VERSION 2.1.0
VERSION_MAJOR 2
VERSION_MINOR 1
VERSION_MICRO 0
*/
/* API */
GLEWAPI GLenum GLEWAPIENTRY glewInit (void);
GLEWAPI GLboolean GLEWAPIENTRY glewIsSupported ( char *name);
#define glewIsExtensionSupported(x) glewIsSupported(x)
#ifndef GLEW_GET_VAR
#define GLEW_GET_VAR(x) (*( GLboolean*)&x)
#endif
#ifndef GLEW_GET_FUN
#define GLEW_GET_FUN(x) x
#endif
GLEWAPI GLboolean glewExperimental;
GLEWAPI GLboolean GLEWAPIENTRY glewGetExtension ( char *name);
GLEWAPI  GLubyte * GLEWAPIENTRY glewGetErrorString (GLenum error);
GLEWAPI  GLubyte * GLEWAPIENTRY glewGetString (GLenum name);
#ifdef __cplusplus
}
#endif
#ifdef GLEW_APIENTRY_DEFINED
#undef GLEW_APIENTRY_DEFINED
#undef APIENTRY
#endif
#ifdef GLEW_CALLBACK_DEFINED
#undef GLEW_CALLBACK_DEFINED
#undef CALLBACK
#endif
#ifdef GLEW_WINGDIAPI_DEFINED
#undef GLEW_WINGDIAPI_DEFINED
#undef WINGDIAPI
#endif
#undef GLAPI
/* #undef GLEWAPI */
#endif /* __glew_h__ */
