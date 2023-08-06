// automatically generated
/*
Copyright (c) 2018 Advanced Micro Devices, Inc. All rights reserved.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
*/

#ifndef INC_KFD_OSTREAM_OPS_H_
#define INC_KFD_OSTREAM_OPS_H_
#ifdef __cplusplus
#include <iostream>

#include "roctracer.h"
#include <string>

namespace roctracer {
namespace kfd_support {
static int KFD_depth_max = 1;
static int KFD_depth_max_cnt = 0;
static std::string KFD_structs_regex = "";
// begin ostream ops for KFD 
// basic ostream ops
template <typename T>
  inline static std::ostream& operator<<(std::ostream& out, const T& v) {
     using std::operator<<;
     static bool recursion = false;
     if (recursion == false) { recursion = true; out << v; recursion = false; }
     return out; }
// End of basic ostream ops

inline static std::ostream& operator<<(std::ostream& out, const HsaVersionInfo& v)
{
  roctracer::kfd_support::operator<<(out, '{');
  KFD_depth_max_cnt++;
  if (KFD_depth_max == -1 || KFD_depth_max_cnt <= KFD_depth_max) {
    if (std::string("HsaVersionInfo::KernelInterfaceMinorVersion").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "KernelInterfaceMinorVersion=");
      roctracer::kfd_support::operator<<(out, v.KernelInterfaceMinorVersion);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaVersionInfo::KernelInterfaceMajorVersion").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "KernelInterfaceMajorVersion=");
      roctracer::kfd_support::operator<<(out, v.KernelInterfaceMajorVersion);
    }
  };
  KFD_depth_max_cnt--;
  roctracer::kfd_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HsaSystemProperties& v)
{
  roctracer::kfd_support::operator<<(out, '{');
  KFD_depth_max_cnt++;
  if (KFD_depth_max == -1 || KFD_depth_max_cnt <= KFD_depth_max) {
    if (std::string("HsaSystemProperties::PlatformRev").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "PlatformRev=");
      roctracer::kfd_support::operator<<(out, v.PlatformRev);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaSystemProperties::PlatformId").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "PlatformId=");
      roctracer::kfd_support::operator<<(out, v.PlatformId);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaSystemProperties::PlatformOem").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "PlatformOem=");
      roctracer::kfd_support::operator<<(out, v.PlatformOem);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaSystemProperties::NumNodes").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "NumNodes=");
      roctracer::kfd_support::operator<<(out, v.NumNodes);
    }
  };
  KFD_depth_max_cnt--;
  roctracer::kfd_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HSA_ENGINE_ID& v)
{
  roctracer::kfd_support::operator<<(out, '{');
  KFD_depth_max_cnt++;
  if (KFD_depth_max == -1 || KFD_depth_max_cnt <= KFD_depth_max) {
    if (std::string("HSA_ENGINE_ID::Value").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "Value=");
      roctracer::kfd_support::operator<<(out, v.Value);
    }
  };
  KFD_depth_max_cnt--;
  roctracer::kfd_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HSA_ENGINE_VERSION& v)
{
  roctracer::kfd_support::operator<<(out, '{');
  KFD_depth_max_cnt++;
  if (KFD_depth_max == -1 || KFD_depth_max_cnt <= KFD_depth_max) {
    if (std::string("HSA_ENGINE_VERSION::Value").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "Value=");
      roctracer::kfd_support::operator<<(out, v.Value);
    }
  };
  KFD_depth_max_cnt--;
  roctracer::kfd_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HSA_CAPABILITY& v)
{
  roctracer::kfd_support::operator<<(out, '{');
  KFD_depth_max_cnt++;
  if (KFD_depth_max == -1 || KFD_depth_max_cnt <= KFD_depth_max) {
    if (std::string("HSA_CAPABILITY::Value").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "Value=");
      roctracer::kfd_support::operator<<(out, v.Value);
    }
  };
  KFD_depth_max_cnt--;
  roctracer::kfd_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HSA_DEBUG_PROPERTIES& v)
{
  roctracer::kfd_support::operator<<(out, '{');
  KFD_depth_max_cnt++;
  if (KFD_depth_max == -1 || KFD_depth_max_cnt <= KFD_depth_max) {
    if (std::string("HSA_DEBUG_PROPERTIES::Value").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "Value=");
      roctracer::kfd_support::operator<<(out, v.Value);
    }
  };
  KFD_depth_max_cnt--;
  roctracer::kfd_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HsaNodeProperties& v)
{
  roctracer::kfd_support::operator<<(out, '{');
  KFD_depth_max_cnt++;
  if (KFD_depth_max == -1 || KFD_depth_max_cnt <= KFD_depth_max) {
    if (std::string("HsaNodeProperties::Reserved").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "Reserved=");
      roctracer::kfd_support::operator<<(out, v.Reserved);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaNodeProperties::SGPRSizePerCU").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "SGPRSizePerCU=");
      roctracer::kfd_support::operator<<(out, v.SGPRSizePerCU);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaNodeProperties::VGPRSizePerCU").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "VGPRSizePerCU=");
      roctracer::kfd_support::operator<<(out, v.VGPRSizePerCU);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaNodeProperties::UniqueID").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "UniqueID=");
      roctracer::kfd_support::operator<<(out, v.UniqueID);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaNodeProperties::Domain").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "Domain=");
      roctracer::kfd_support::operator<<(out, v.Domain);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaNodeProperties::Reserved2").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "Reserved2=");
      roctracer::kfd_support::operator<<(out, v.Reserved2);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaNodeProperties::NumGws").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "NumGws=");
      roctracer::kfd_support::operator<<(out, v.NumGws);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaNodeProperties::NumCpQueues").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "NumCpQueues=");
      roctracer::kfd_support::operator<<(out, v.NumCpQueues);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaNodeProperties::NumSdmaQueuesPerEngine").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "NumSdmaQueuesPerEngine=");
      roctracer::kfd_support::operator<<(out, v.NumSdmaQueuesPerEngine);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaNodeProperties::NumSdmaXgmiEngines").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "NumSdmaXgmiEngines=");
      roctracer::kfd_support::operator<<(out, v.NumSdmaXgmiEngines);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaNodeProperties::NumSdmaEngines").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "NumSdmaEngines=");
      roctracer::kfd_support::operator<<(out, v.NumSdmaEngines);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaNodeProperties::HiveID").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "HiveID=");
      roctracer::kfd_support::operator<<(out, v.HiveID);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaNodeProperties::DebugProperties").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "DebugProperties=");
      roctracer::kfd_support::operator<<(out, v.DebugProperties);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaNodeProperties::uCodeEngineVersions").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "uCodeEngineVersions=");
      roctracer::kfd_support::operator<<(out, v.uCodeEngineVersions);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaNodeProperties::AMDName").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "AMDName=");
      roctracer::kfd_support::operator<<(out, v.AMDName);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaNodeProperties::MarketingName").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "MarketingName=");
      roctracer::kfd_support::operator<<(out, v.MarketingName);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaNodeProperties::DrmRenderMinor").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "DrmRenderMinor=");
      roctracer::kfd_support::operator<<(out, v.DrmRenderMinor);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaNodeProperties::MaxEngineClockMhzCCompute").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "MaxEngineClockMhzCCompute=");
      roctracer::kfd_support::operator<<(out, v.MaxEngineClockMhzCCompute);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaNodeProperties::MaxEngineClockMhzFCompute").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "MaxEngineClockMhzFCompute=");
      roctracer::kfd_support::operator<<(out, v.MaxEngineClockMhzFCompute);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaNodeProperties::LocalMemSize").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "LocalMemSize=");
      roctracer::kfd_support::operator<<(out, v.LocalMemSize);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaNodeProperties::LocationId").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "LocationId=");
      roctracer::kfd_support::operator<<(out, v.LocationId);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaNodeProperties::DeviceId").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "DeviceId=");
      roctracer::kfd_support::operator<<(out, v.DeviceId);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaNodeProperties::VendorId").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "VendorId=");
      roctracer::kfd_support::operator<<(out, v.VendorId);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaNodeProperties::EngineId").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "EngineId=");
      roctracer::kfd_support::operator<<(out, v.EngineId);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaNodeProperties::MaxSlotsScratchCU").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "MaxSlotsScratchCU=");
      roctracer::kfd_support::operator<<(out, v.MaxSlotsScratchCU);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaNodeProperties::NumSIMDPerCU").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "NumSIMDPerCU=");
      roctracer::kfd_support::operator<<(out, v.NumSIMDPerCU);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaNodeProperties::NumCUPerArray").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "NumCUPerArray=");
      roctracer::kfd_support::operator<<(out, v.NumCUPerArray);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaNodeProperties::NumArrays").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "NumArrays=");
      roctracer::kfd_support::operator<<(out, v.NumArrays);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaNodeProperties::NumShaderBanks").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "NumShaderBanks=");
      roctracer::kfd_support::operator<<(out, v.NumShaderBanks);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaNodeProperties::WaveFrontSize").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "WaveFrontSize=");
      roctracer::kfd_support::operator<<(out, v.WaveFrontSize);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaNodeProperties::GDSSizeInKB").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "GDSSizeInKB=");
      roctracer::kfd_support::operator<<(out, v.GDSSizeInKB);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaNodeProperties::LDSSizeInKB").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "LDSSizeInKB=");
      roctracer::kfd_support::operator<<(out, v.LDSSizeInKB);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaNodeProperties::MaxWavesPerSIMD").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "MaxWavesPerSIMD=");
      roctracer::kfd_support::operator<<(out, v.MaxWavesPerSIMD);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaNodeProperties::Capability").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "Capability=");
      roctracer::kfd_support::operator<<(out, v.Capability);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaNodeProperties::FComputeIdLo").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "FComputeIdLo=");
      roctracer::kfd_support::operator<<(out, v.FComputeIdLo);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaNodeProperties::CComputeIdLo").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "CComputeIdLo=");
      roctracer::kfd_support::operator<<(out, v.CComputeIdLo);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaNodeProperties::NumIOLinks").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "NumIOLinks=");
      roctracer::kfd_support::operator<<(out, v.NumIOLinks);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaNodeProperties::NumCaches").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "NumCaches=");
      roctracer::kfd_support::operator<<(out, v.NumCaches);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaNodeProperties::NumMemoryBanks").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "NumMemoryBanks=");
      roctracer::kfd_support::operator<<(out, v.NumMemoryBanks);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaNodeProperties::NumFComputeCores").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "NumFComputeCores=");
      roctracer::kfd_support::operator<<(out, v.NumFComputeCores);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaNodeProperties::NumCPUCores").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "NumCPUCores=");
      roctracer::kfd_support::operator<<(out, v.NumCPUCores);
    }
  };
  KFD_depth_max_cnt--;
  roctracer::kfd_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HSA_MEMORYPROPERTY& v)
{
  roctracer::kfd_support::operator<<(out, '{');
  KFD_depth_max_cnt++;
  if (KFD_depth_max == -1 || KFD_depth_max_cnt <= KFD_depth_max) {
    if (std::string("HSA_MEMORYPROPERTY::MemoryProperty").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "MemoryProperty=");
      roctracer::kfd_support::operator<<(out, v.MemoryProperty);
    }
  };
  KFD_depth_max_cnt--;
  roctracer::kfd_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HsaMemoryProperties& v)
{
  roctracer::kfd_support::operator<<(out, '{');
  KFD_depth_max_cnt++;
  if (KFD_depth_max == -1 || KFD_depth_max_cnt <= KFD_depth_max) {
    if (std::string("HsaMemoryProperties::VirtualBaseAddress").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "VirtualBaseAddress=");
      roctracer::kfd_support::operator<<(out, v.VirtualBaseAddress);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaMemoryProperties::MemoryClockMax").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "MemoryClockMax=");
      roctracer::kfd_support::operator<<(out, v.MemoryClockMax);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaMemoryProperties::Width").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "Width=");
      roctracer::kfd_support::operator<<(out, v.Width);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaMemoryProperties::Flags").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "Flags=");
      roctracer::kfd_support::operator<<(out, v.Flags);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaMemoryProperties::HeapType").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "HeapType=");
      roctracer::kfd_support::operator<<(out, v.HeapType);
    }
  };
  KFD_depth_max_cnt--;
  roctracer::kfd_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HsaCacheType& v)
{
  roctracer::kfd_support::operator<<(out, '{');
  KFD_depth_max_cnt++;
  if (KFD_depth_max == -1 || KFD_depth_max_cnt <= KFD_depth_max) {
    if (std::string("HsaCacheType::Value").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "Value=");
      roctracer::kfd_support::operator<<(out, v.Value);
    }
  };
  KFD_depth_max_cnt--;
  roctracer::kfd_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HsaCacheProperties& v)
{
  roctracer::kfd_support::operator<<(out, '{');
  KFD_depth_max_cnt++;
  if (KFD_depth_max == -1 || KFD_depth_max_cnt <= KFD_depth_max) {
    if (std::string("HsaCacheProperties::SiblingMap").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "SiblingMap=");
      roctracer::kfd_support::operator<<(out, v.SiblingMap);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaCacheProperties::CacheType").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "CacheType=");
      roctracer::kfd_support::operator<<(out, v.CacheType);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaCacheProperties::CacheLatency").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "CacheLatency=");
      roctracer::kfd_support::operator<<(out, v.CacheLatency);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaCacheProperties::CacheAssociativity").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "CacheAssociativity=");
      roctracer::kfd_support::operator<<(out, v.CacheAssociativity);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaCacheProperties::CacheLinesPerTag").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "CacheLinesPerTag=");
      roctracer::kfd_support::operator<<(out, v.CacheLinesPerTag);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaCacheProperties::CacheLineSize").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "CacheLineSize=");
      roctracer::kfd_support::operator<<(out, v.CacheLineSize);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaCacheProperties::CacheSize").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "CacheSize=");
      roctracer::kfd_support::operator<<(out, v.CacheSize);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaCacheProperties::CacheLevel").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "CacheLevel=");
      roctracer::kfd_support::operator<<(out, v.CacheLevel);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaCacheProperties::ProcessorIdLow").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "ProcessorIdLow=");
      roctracer::kfd_support::operator<<(out, v.ProcessorIdLow);
    }
  };
  KFD_depth_max_cnt--;
  roctracer::kfd_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HsaCComputeProperties& v)
{
  roctracer::kfd_support::operator<<(out, '{');
  KFD_depth_max_cnt++;
  if (KFD_depth_max == -1 || KFD_depth_max_cnt <= KFD_depth_max) {
    if (std::string("HsaCComputeProperties::SiblingMap").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "SiblingMap=");
      roctracer::kfd_support::operator<<(out, v.SiblingMap);
    }
  };
  KFD_depth_max_cnt--;
  roctracer::kfd_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HSA_LINKPROPERTY& v)
{
  roctracer::kfd_support::operator<<(out, '{');
  KFD_depth_max_cnt++;
  if (KFD_depth_max == -1 || KFD_depth_max_cnt <= KFD_depth_max) {
    if (std::string("HSA_LINKPROPERTY::LinkProperty").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "LinkProperty=");
      roctracer::kfd_support::operator<<(out, v.LinkProperty);
    }
  };
  KFD_depth_max_cnt--;
  roctracer::kfd_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HsaIoLinkProperties& v)
{
  roctracer::kfd_support::operator<<(out, '{');
  KFD_depth_max_cnt++;
  if (KFD_depth_max == -1 || KFD_depth_max_cnt <= KFD_depth_max) {
    if (std::string("HsaIoLinkProperties::Flags").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "Flags=");
      roctracer::kfd_support::operator<<(out, v.Flags);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaIoLinkProperties::RecTransferSize").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "RecTransferSize=");
      roctracer::kfd_support::operator<<(out, v.RecTransferSize);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaIoLinkProperties::MaximumBandwidth").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "MaximumBandwidth=");
      roctracer::kfd_support::operator<<(out, v.MaximumBandwidth);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaIoLinkProperties::MinimumBandwidth").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "MinimumBandwidth=");
      roctracer::kfd_support::operator<<(out, v.MinimumBandwidth);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaIoLinkProperties::MaximumLatency").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "MaximumLatency=");
      roctracer::kfd_support::operator<<(out, v.MaximumLatency);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaIoLinkProperties::MinimumLatency").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "MinimumLatency=");
      roctracer::kfd_support::operator<<(out, v.MinimumLatency);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaIoLinkProperties::Weight").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "Weight=");
      roctracer::kfd_support::operator<<(out, v.Weight);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaIoLinkProperties::NodeTo").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "NodeTo=");
      roctracer::kfd_support::operator<<(out, v.NodeTo);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaIoLinkProperties::NodeFrom").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "NodeFrom=");
      roctracer::kfd_support::operator<<(out, v.NodeFrom);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaIoLinkProperties::VersionMinor").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "VersionMinor=");
      roctracer::kfd_support::operator<<(out, v.VersionMinor);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaIoLinkProperties::VersionMajor").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "VersionMajor=");
      roctracer::kfd_support::operator<<(out, v.VersionMajor);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaIoLinkProperties::IoLinkType").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "IoLinkType=");
      roctracer::kfd_support::operator<<(out, v.IoLinkType);
    }
  };
  KFD_depth_max_cnt--;
  roctracer::kfd_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HsaMemFlags& v)
{
  roctracer::kfd_support::operator<<(out, '{');
  KFD_depth_max_cnt++;
  if (KFD_depth_max == -1 || KFD_depth_max_cnt <= KFD_depth_max) {
  };
  KFD_depth_max_cnt--;
  roctracer::kfd_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HsaMemMapFlags& v)
{
  roctracer::kfd_support::operator<<(out, '{');
  KFD_depth_max_cnt++;
  if (KFD_depth_max == -1 || KFD_depth_max_cnt <= KFD_depth_max) {
  };
  KFD_depth_max_cnt--;
  roctracer::kfd_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HsaGraphicsResourceInfo& v)
{
  roctracer::kfd_support::operator<<(out, '{');
  KFD_depth_max_cnt++;
  if (KFD_depth_max == -1 || KFD_depth_max_cnt <= KFD_depth_max) {
    if (std::string("HsaGraphicsResourceInfo::Reserved").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "Reserved=");
      roctracer::kfd_support::operator<<(out, v.Reserved);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaGraphicsResourceInfo::MetadataSizeInBytes").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "MetadataSizeInBytes=");
      roctracer::kfd_support::operator<<(out, v.MetadataSizeInBytes);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaGraphicsResourceInfo::SizeInBytes").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "SizeInBytes=");
      roctracer::kfd_support::operator<<(out, v.SizeInBytes);
    }
  };
  KFD_depth_max_cnt--;
  roctracer::kfd_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HsaUserContextSaveAreaHeader& v)
{
  roctracer::kfd_support::operator<<(out, '{');
  KFD_depth_max_cnt++;
  if (KFD_depth_max == -1 || KFD_depth_max_cnt <= KFD_depth_max) {
    if (std::string("HsaUserContextSaveAreaHeader::DebugSize").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "DebugSize=");
      roctracer::kfd_support::operator<<(out, v.DebugSize);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaUserContextSaveAreaHeader::DebugOffset").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "DebugOffset=");
      roctracer::kfd_support::operator<<(out, v.DebugOffset);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaUserContextSaveAreaHeader::WaveStateSize").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "WaveStateSize=");
      roctracer::kfd_support::operator<<(out, v.WaveStateSize);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaUserContextSaveAreaHeader::WaveStateOffset").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "WaveStateOffset=");
      roctracer::kfd_support::operator<<(out, v.WaveStateOffset);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaUserContextSaveAreaHeader::ControlStackSize").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "ControlStackSize=");
      roctracer::kfd_support::operator<<(out, v.ControlStackSize);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaUserContextSaveAreaHeader::ControlStackOffset").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "ControlStackOffset=");
      roctracer::kfd_support::operator<<(out, v.ControlStackOffset);
    }
  };
  KFD_depth_max_cnt--;
  roctracer::kfd_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HsaQueueInfo& v)
{
  roctracer::kfd_support::operator<<(out, '{');
  KFD_depth_max_cnt++;
  if (KFD_depth_max == -1 || KFD_depth_max_cnt <= KFD_depth_max) {
    if (std::string("HsaQueueInfo::Reserved2").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "Reserved2=");
      roctracer::kfd_support::operator<<(out, v.Reserved2);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaQueueInfo::SaveAreaHeader").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "SaveAreaHeader=");
      roctracer::kfd_support::operator<<(out, v.SaveAreaHeader);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaQueueInfo::ControlStackUsedInBytes").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "ControlStackUsedInBytes=");
      roctracer::kfd_support::operator<<(out, v.ControlStackUsedInBytes);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaQueueInfo::ControlStackTop").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "ControlStackTop=");
      roctracer::kfd_support::operator<<(out, v.ControlStackTop);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaQueueInfo::SaveAreaSizeInBytes").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "SaveAreaSizeInBytes=");
      roctracer::kfd_support::operator<<(out, v.SaveAreaSizeInBytes);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaQueueInfo::UserContextSaveArea").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "UserContextSaveArea=");
      roctracer::kfd_support::operator<<(out, v.UserContextSaveArea);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaQueueInfo::CUMaskInfo").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "CUMaskInfo=");
      roctracer::kfd_support::operator<<(out, v.CUMaskInfo);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaQueueInfo::NumCUAssigned").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "NumCUAssigned=");
      roctracer::kfd_support::operator<<(out, v.NumCUAssigned);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaQueueInfo::QueueTypeExtended").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "QueueTypeExtended=");
      roctracer::kfd_support::operator<<(out, v.QueueTypeExtended);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaQueueInfo::QueueDetailError").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "QueueDetailError=");
      roctracer::kfd_support::operator<<(out, v.QueueDetailError);
    }
  };
  KFD_depth_max_cnt--;
  roctracer::kfd_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HsaQueueResource& v)
{
  roctracer::kfd_support::operator<<(out, '{');
  KFD_depth_max_cnt++;
  if (KFD_depth_max == -1 || KFD_depth_max_cnt <= KFD_depth_max) {
    if (std::string("HsaQueueResource::QueueId").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "QueueId=");
      roctracer::kfd_support::operator<<(out, v.QueueId);
    }
  };
  KFD_depth_max_cnt--;
  roctracer::kfd_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HsaQueueReport& v)
{
  roctracer::kfd_support::operator<<(out, '{');
  KFD_depth_max_cnt++;
  if (KFD_depth_max == -1 || KFD_depth_max_cnt <= KFD_depth_max) {
    if (std::string("HsaQueueReport::QueueSize").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "QueueSize=");
      roctracer::kfd_support::operator<<(out, v.QueueSize);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaQueueReport::VMID").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "VMID=");
      roctracer::kfd_support::operator<<(out, v.VMID);
    }
  };
  KFD_depth_max_cnt--;
  roctracer::kfd_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HsaDbgWaveMsgAMDGen2& v)
{
  roctracer::kfd_support::operator<<(out, '{');
  KFD_depth_max_cnt++;
  if (KFD_depth_max == -1 || KFD_depth_max_cnt <= KFD_depth_max) {
    if (std::string("HsaDbgWaveMsgAMDGen2::Reserved2").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "Reserved2=");
      roctracer::kfd_support::operator<<(out, v.Reserved2);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaDbgWaveMsgAMDGen2::Value").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "Value=");
      roctracer::kfd_support::operator<<(out, v.Value);
    }
  };
  KFD_depth_max_cnt--;
  roctracer::kfd_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HsaDbgWaveMessageAMD& v)
{
  roctracer::kfd_support::operator<<(out, '{');
  KFD_depth_max_cnt++;
  if (KFD_depth_max == -1 || KFD_depth_max_cnt <= KFD_depth_max) {
    if (std::string("HsaDbgWaveMessageAMD::WaveMsgInfoGen2").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "WaveMsgInfoGen2=");
      roctracer::kfd_support::operator<<(out, v.WaveMsgInfoGen2);
    }
  };
  KFD_depth_max_cnt--;
  roctracer::kfd_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HsaDbgWaveMessage& v)
{
  roctracer::kfd_support::operator<<(out, '{');
  KFD_depth_max_cnt++;
  if (KFD_depth_max == -1 || KFD_depth_max_cnt <= KFD_depth_max) {
    if (std::string("HsaDbgWaveMessage::DbgWaveMsg").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "DbgWaveMsg=");
      roctracer::kfd_support::operator<<(out, v.DbgWaveMsg);
    }
  };
  KFD_depth_max_cnt--;
  roctracer::kfd_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HsaSyncVar& v)
{
  roctracer::kfd_support::operator<<(out, '{');
  KFD_depth_max_cnt++;
  if (KFD_depth_max == -1 || KFD_depth_max_cnt <= KFD_depth_max) {
    if (std::string("HsaSyncVar::SyncVarSize").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "SyncVarSize=");
      roctracer::kfd_support::operator<<(out, v.SyncVarSize);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("_HsaSyncVar::union ::SyncVar.UserDataPtrValue").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "SyncVar.UserDataPtrValue=");
      roctracer::kfd_support::operator<<(out, v.SyncVar.UserDataPtrValue);
    }
  };
  KFD_depth_max_cnt--;
  roctracer::kfd_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HsaNodeChange& v)
{
  roctracer::kfd_support::operator<<(out, '{');
  KFD_depth_max_cnt++;
  if (KFD_depth_max == -1 || KFD_depth_max_cnt <= KFD_depth_max) {
    if (std::string("HsaNodeChange::Flags").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "Flags=");
      roctracer::kfd_support::operator<<(out, v.Flags);
    }
  };
  KFD_depth_max_cnt--;
  roctracer::kfd_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HsaDeviceStateChange& v)
{
  roctracer::kfd_support::operator<<(out, '{');
  KFD_depth_max_cnt++;
  if (KFD_depth_max == -1 || KFD_depth_max_cnt <= KFD_depth_max) {
    if (std::string("HsaDeviceStateChange::Flags").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "Flags=");
      roctracer::kfd_support::operator<<(out, v.Flags);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaDeviceStateChange::Device").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "Device=");
      roctracer::kfd_support::operator<<(out, v.Device);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaDeviceStateChange::NodeId").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "NodeId=");
      roctracer::kfd_support::operator<<(out, v.NodeId);
    }
  };
  KFD_depth_max_cnt--;
  roctracer::kfd_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HsaAccessAttributeFailure& v)
{
  roctracer::kfd_support::operator<<(out, '{');
  KFD_depth_max_cnt++;
  if (KFD_depth_max == -1 || KFD_depth_max_cnt <= KFD_depth_max) {
    if (std::string("HsaAccessAttributeFailure::Reserved").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "Reserved=");
      roctracer::kfd_support::operator<<(out, v.Reserved);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaAccessAttributeFailure::ErrorType").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "ErrorType=");
      roctracer::kfd_support::operator<<(out, v.ErrorType);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaAccessAttributeFailure::Imprecise").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "Imprecise=");
      roctracer::kfd_support::operator<<(out, v.Imprecise);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaAccessAttributeFailure::ECC").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "ECC=");
      roctracer::kfd_support::operator<<(out, v.ECC);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaAccessAttributeFailure::GpuAccess").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "GpuAccess=");
      roctracer::kfd_support::operator<<(out, v.GpuAccess);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaAccessAttributeFailure::NoExecute").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "NoExecute=");
      roctracer::kfd_support::operator<<(out, v.NoExecute);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaAccessAttributeFailure::ReadOnly").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "ReadOnly=");
      roctracer::kfd_support::operator<<(out, v.ReadOnly);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaAccessAttributeFailure::NotPresent").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "NotPresent=");
      roctracer::kfd_support::operator<<(out, v.NotPresent);
    }
  };
  KFD_depth_max_cnt--;
  roctracer::kfd_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HsaMemoryAccessFault& v)
{
  roctracer::kfd_support::operator<<(out, '{');
  KFD_depth_max_cnt++;
  if (KFD_depth_max == -1 || KFD_depth_max_cnt <= KFD_depth_max) {
    if (std::string("HsaMemoryAccessFault::Flags").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "Flags=");
      roctracer::kfd_support::operator<<(out, v.Flags);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaMemoryAccessFault::Failure").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "Failure=");
      roctracer::kfd_support::operator<<(out, v.Failure);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaMemoryAccessFault::VirtualAddress").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "VirtualAddress=");
      roctracer::kfd_support::operator<<(out, v.VirtualAddress);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaMemoryAccessFault::NodeId").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "NodeId=");
      roctracer::kfd_support::operator<<(out, v.NodeId);
    }
  };
  KFD_depth_max_cnt--;
  roctracer::kfd_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HsaEventData& v)
{
  roctracer::kfd_support::operator<<(out, '{');
  KFD_depth_max_cnt++;
  if (KFD_depth_max == -1 || KFD_depth_max_cnt <= KFD_depth_max) {
    if (std::string("HsaEventData::HWData3").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "HWData3=");
      roctracer::kfd_support::operator<<(out, v.HWData3);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaEventData::HWData2").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "HWData2=");
      roctracer::kfd_support::operator<<(out, v.HWData2);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaEventData::HWData1").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "HWData1=");
      roctracer::kfd_support::operator<<(out, v.HWData1);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("_HsaEventData::union ::EventData.MemoryAccessFault").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "EventData.MemoryAccessFault=");
      roctracer::kfd_support::operator<<(out, v.EventData.MemoryAccessFault);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("_HsaEventData::union ::EventData.DeviceState").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "EventData.DeviceState=");
      roctracer::kfd_support::operator<<(out, v.EventData.DeviceState);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("_HsaEventData::union ::EventData.NodeChangeState").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "EventData.NodeChangeState=");
      roctracer::kfd_support::operator<<(out, v.EventData.NodeChangeState);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("_HsaEventData::union ::EventData.SyncVar").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "EventData.SyncVar=");
      roctracer::kfd_support::operator<<(out, v.EventData.SyncVar);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaEventData::EventType").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "EventType=");
      roctracer::kfd_support::operator<<(out, v.EventType);
    }
  };
  KFD_depth_max_cnt--;
  roctracer::kfd_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HsaEventDescriptor& v)
{
  roctracer::kfd_support::operator<<(out, '{');
  KFD_depth_max_cnt++;
  if (KFD_depth_max == -1 || KFD_depth_max_cnt <= KFD_depth_max) {
    if (std::string("HsaEventDescriptor::SyncVar").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "SyncVar=");
      roctracer::kfd_support::operator<<(out, v.SyncVar);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaEventDescriptor::NodeId").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "NodeId=");
      roctracer::kfd_support::operator<<(out, v.NodeId);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaEventDescriptor::EventType").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "EventType=");
      roctracer::kfd_support::operator<<(out, v.EventType);
    }
  };
  KFD_depth_max_cnt--;
  roctracer::kfd_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HsaEvent& v)
{
  roctracer::kfd_support::operator<<(out, '{');
  KFD_depth_max_cnt++;
  if (KFD_depth_max == -1 || KFD_depth_max_cnt <= KFD_depth_max) {
    if (std::string("HsaEvent::EventData").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "EventData=");
      roctracer::kfd_support::operator<<(out, v.EventData);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaEvent::EventId").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "EventId=");
      roctracer::kfd_support::operator<<(out, v.EventId);
    }
  };
  KFD_depth_max_cnt--;
  roctracer::kfd_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HsaClockCounters& v)
{
  roctracer::kfd_support::operator<<(out, '{');
  KFD_depth_max_cnt++;
  if (KFD_depth_max == -1 || KFD_depth_max_cnt <= KFD_depth_max) {
    if (std::string("HsaClockCounters::SystemClockFrequencyHz").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "SystemClockFrequencyHz=");
      roctracer::kfd_support::operator<<(out, v.SystemClockFrequencyHz);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaClockCounters::SystemClockCounter").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "SystemClockCounter=");
      roctracer::kfd_support::operator<<(out, v.SystemClockCounter);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaClockCounters::CPUClockCounter").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "CPUClockCounter=");
      roctracer::kfd_support::operator<<(out, v.CPUClockCounter);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaClockCounters::GPUClockCounter").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "GPUClockCounter=");
      roctracer::kfd_support::operator<<(out, v.GPUClockCounter);
    }
  };
  KFD_depth_max_cnt--;
  roctracer::kfd_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HSA_UUID& v)
{
  roctracer::kfd_support::operator<<(out, '{');
  KFD_depth_max_cnt++;
  if (KFD_depth_max == -1 || KFD_depth_max_cnt <= KFD_depth_max) {
    if (std::string("HSA_UUID::Data4").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "Data4=");
      roctracer::kfd_support::operator<<(out, v.Data4);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HSA_UUID::Data3").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "Data3=");
      roctracer::kfd_support::operator<<(out, v.Data3);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HSA_UUID::Data2").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "Data2=");
      roctracer::kfd_support::operator<<(out, v.Data2);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HSA_UUID::Data1").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "Data1=");
      roctracer::kfd_support::operator<<(out, v.Data1);
    }
  };
  KFD_depth_max_cnt--;
  roctracer::kfd_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HsaCounterFlags& v)
{
  roctracer::kfd_support::operator<<(out, '{');
  KFD_depth_max_cnt++;
  if (KFD_depth_max == -1 || KFD_depth_max_cnt <= KFD_depth_max) {
  };
  KFD_depth_max_cnt--;
  roctracer::kfd_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HsaCounter& v)
{
  roctracer::kfd_support::operator<<(out, '{');
  KFD_depth_max_cnt++;
  if (KFD_depth_max == -1 || KFD_depth_max_cnt <= KFD_depth_max) {
    if (std::string("HsaCounter::BlockIndex").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "BlockIndex=");
      roctracer::kfd_support::operator<<(out, v.BlockIndex);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaCounter::Flags").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "Flags=");
      roctracer::kfd_support::operator<<(out, v.Flags);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaCounter::CounterMask").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "CounterMask=");
      roctracer::kfd_support::operator<<(out, v.CounterMask);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaCounter::CounterSizeInBits").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "CounterSizeInBits=");
      roctracer::kfd_support::operator<<(out, v.CounterSizeInBits);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaCounter::CounterId").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "CounterId=");
      roctracer::kfd_support::operator<<(out, v.CounterId);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaCounter::Type").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "Type=");
      roctracer::kfd_support::operator<<(out, v.Type);
    }
  };
  KFD_depth_max_cnt--;
  roctracer::kfd_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HsaCounterBlockProperties& v)
{
  roctracer::kfd_support::operator<<(out, '{');
  KFD_depth_max_cnt++;
  if (KFD_depth_max == -1 || KFD_depth_max_cnt <= KFD_depth_max) {
    if (std::string("HsaCounterBlockProperties::Counters").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "Counters=");
      roctracer::kfd_support::operator<<(out, v.Counters);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaCounterBlockProperties::NumConcurrent").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "NumConcurrent=");
      roctracer::kfd_support::operator<<(out, v.NumConcurrent);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaCounterBlockProperties::NumCounters").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "NumCounters=");
      roctracer::kfd_support::operator<<(out, v.NumCounters);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaCounterBlockProperties::BlockId").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "BlockId=");
      roctracer::kfd_support::operator<<(out, v.BlockId);
    }
  };
  KFD_depth_max_cnt--;
  roctracer::kfd_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HsaCounterProperties& v)
{
  roctracer::kfd_support::operator<<(out, '{');
  KFD_depth_max_cnt++;
  if (KFD_depth_max == -1 || KFD_depth_max_cnt <= KFD_depth_max) {
    if (std::string("HsaCounterProperties::Blocks").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "Blocks=");
      roctracer::kfd_support::operator<<(out, v.Blocks);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaCounterProperties::NumConcurrent").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "NumConcurrent=");
      roctracer::kfd_support::operator<<(out, v.NumConcurrent);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaCounterProperties::NumBlocks").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "NumBlocks=");
      roctracer::kfd_support::operator<<(out, v.NumBlocks);
    }
  };
  KFD_depth_max_cnt--;
  roctracer::kfd_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HsaPmcTraceRoot& v)
{
  roctracer::kfd_support::operator<<(out, '{');
  KFD_depth_max_cnt++;
  if (KFD_depth_max == -1 || KFD_depth_max_cnt <= KFD_depth_max) {
    if (std::string("HsaPmcTraceRoot::TraceId").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "TraceId=");
      roctracer::kfd_support::operator<<(out, v.TraceId);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaPmcTraceRoot::NumberOfPasses").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "NumberOfPasses=");
      roctracer::kfd_support::operator<<(out, v.NumberOfPasses);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaPmcTraceRoot::TraceBufferMinSizeBytes").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "TraceBufferMinSizeBytes=");
      roctracer::kfd_support::operator<<(out, v.TraceBufferMinSizeBytes);
    }
  };
  KFD_depth_max_cnt--;
  roctracer::kfd_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HsaGpuTileConfig& v)
{
  roctracer::kfd_support::operator<<(out, '{');
  KFD_depth_max_cnt++;
  if (KFD_depth_max == -1 || KFD_depth_max_cnt <= KFD_depth_max) {
    if (std::string("HsaGpuTileConfig::Reserved").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "Reserved=");
      roctracer::kfd_support::operator<<(out, v.Reserved);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaGpuTileConfig::NumRanks").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "NumRanks=");
      roctracer::kfd_support::operator<<(out, v.NumRanks);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaGpuTileConfig::NumBanks").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "NumBanks=");
      roctracer::kfd_support::operator<<(out, v.NumBanks);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaGpuTileConfig::GbAddrConfig").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "GbAddrConfig=");
      roctracer::kfd_support::operator<<(out, v.GbAddrConfig);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaGpuTileConfig::NumMacroTileConfigs").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "NumMacroTileConfigs=");
      roctracer::kfd_support::operator<<(out, v.NumMacroTileConfigs);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaGpuTileConfig::NumTileConfigs").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "NumTileConfigs=");
      roctracer::kfd_support::operator<<(out, v.NumTileConfigs);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaGpuTileConfig::MacroTileConfig").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "MacroTileConfig=");
      roctracer::kfd_support::operator<<(out, v.MacroTileConfig);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaGpuTileConfig::TileConfig").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "TileConfig=");
      roctracer::kfd_support::operator<<(out, v.TileConfig);
    }
  };
  KFD_depth_max_cnt--;
  roctracer::kfd_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HsaPointerInfo& v)
{
  roctracer::kfd_support::operator<<(out, '{');
  KFD_depth_max_cnt++;
  if (KFD_depth_max == -1 || KFD_depth_max_cnt <= KFD_depth_max) {
    if (std::string("HsaPointerInfo::MappedNodes").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "MappedNodes=");
      roctracer::kfd_support::operator<<(out, v.MappedNodes);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaPointerInfo::RegisteredNodes").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "RegisteredNodes=");
      roctracer::kfd_support::operator<<(out, v.RegisteredNodes);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaPointerInfo::NMappedNodes").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "NMappedNodes=");
      roctracer::kfd_support::operator<<(out, v.NMappedNodes);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaPointerInfo::NRegisteredNodes").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "NRegisteredNodes=");
      roctracer::kfd_support::operator<<(out, v.NRegisteredNodes);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaPointerInfo::SizeInBytes").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "SizeInBytes=");
      roctracer::kfd_support::operator<<(out, v.SizeInBytes);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaPointerInfo::GPUAddress").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "GPUAddress=");
      roctracer::kfd_support::operator<<(out, v.GPUAddress);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaPointerInfo::MemFlags").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "MemFlags=");
      roctracer::kfd_support::operator<<(out, v.MemFlags);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaPointerInfo::Node").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "Node=");
      roctracer::kfd_support::operator<<(out, v.Node);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HsaPointerInfo::Type").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "Type=");
      roctracer::kfd_support::operator<<(out, v.Type);
    }
  };
  KFD_depth_max_cnt--;
  roctracer::kfd_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HsaMemoryRange& v)
{
  roctracer::kfd_support::operator<<(out, '{');
  KFD_depth_max_cnt++;
  if (KFD_depth_max == -1 || KFD_depth_max_cnt <= KFD_depth_max) {
    if (std::string("HsaMemoryRange::SizeInBytes").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "SizeInBytes=");
      roctracer::kfd_support::operator<<(out, v.SizeInBytes);
    }
  };
  KFD_depth_max_cnt--;
  roctracer::kfd_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HSA_SVM_ATTRIBUTE& v)
{
  roctracer::kfd_support::operator<<(out, '{');
  KFD_depth_max_cnt++;
  if (KFD_depth_max == -1 || KFD_depth_max_cnt <= KFD_depth_max) {
    if (std::string("HSA_SVM_ATTRIBUTE::value").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "value=");
      roctracer::kfd_support::operator<<(out, v.value);
      roctracer::kfd_support::operator<<(out, ", ");
    }
    if (std::string("HSA_SVM_ATTRIBUTE::type").find(KFD_structs_regex) != std::string::npos)   {
      roctracer::kfd_support::operator<<(out, "type=");
      roctracer::kfd_support::operator<<(out, v.type);
    }
  };
  KFD_depth_max_cnt--;
  roctracer::kfd_support::operator<<(out, '}');
  return out;
}
// end ostream ops for KFD 
};};

inline static std::ostream& operator<<(std::ostream& out, const HsaVersionInfo& v)
{
  roctracer::kfd_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HsaSystemProperties& v)
{
  roctracer::kfd_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HSA_ENGINE_ID& v)
{
  roctracer::kfd_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HSA_ENGINE_VERSION& v)
{
  roctracer::kfd_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HSA_CAPABILITY& v)
{
  roctracer::kfd_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HSA_DEBUG_PROPERTIES& v)
{
  roctracer::kfd_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HsaNodeProperties& v)
{
  roctracer::kfd_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HSA_MEMORYPROPERTY& v)
{
  roctracer::kfd_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HsaMemoryProperties& v)
{
  roctracer::kfd_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HsaCacheType& v)
{
  roctracer::kfd_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HsaCacheProperties& v)
{
  roctracer::kfd_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HsaCComputeProperties& v)
{
  roctracer::kfd_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HSA_LINKPROPERTY& v)
{
  roctracer::kfd_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HsaIoLinkProperties& v)
{
  roctracer::kfd_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HsaMemFlags& v)
{
  roctracer::kfd_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HsaMemMapFlags& v)
{
  roctracer::kfd_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HsaGraphicsResourceInfo& v)
{
  roctracer::kfd_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HsaUserContextSaveAreaHeader& v)
{
  roctracer::kfd_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HsaQueueInfo& v)
{
  roctracer::kfd_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HsaQueueResource& v)
{
  roctracer::kfd_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HsaQueueReport& v)
{
  roctracer::kfd_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HsaDbgWaveMsgAMDGen2& v)
{
  roctracer::kfd_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HsaDbgWaveMessageAMD& v)
{
  roctracer::kfd_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HsaDbgWaveMessage& v)
{
  roctracer::kfd_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HsaSyncVar& v)
{
  roctracer::kfd_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HsaNodeChange& v)
{
  roctracer::kfd_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HsaDeviceStateChange& v)
{
  roctracer::kfd_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HsaAccessAttributeFailure& v)
{
  roctracer::kfd_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HsaMemoryAccessFault& v)
{
  roctracer::kfd_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HsaEventData& v)
{
  roctracer::kfd_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HsaEventDescriptor& v)
{
  roctracer::kfd_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HsaEvent& v)
{
  roctracer::kfd_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HsaClockCounters& v)
{
  roctracer::kfd_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HSA_UUID& v)
{
  roctracer::kfd_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HsaCounterFlags& v)
{
  roctracer::kfd_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HsaCounter& v)
{
  roctracer::kfd_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HsaCounterBlockProperties& v)
{
  roctracer::kfd_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HsaCounterProperties& v)
{
  roctracer::kfd_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HsaPmcTraceRoot& v)
{
  roctracer::kfd_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HsaGpuTileConfig& v)
{
  roctracer::kfd_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HsaPointerInfo& v)
{
  roctracer::kfd_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HsaMemoryRange& v)
{
  roctracer::kfd_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HSA_SVM_ATTRIBUTE& v)
{
  roctracer::kfd_support::operator<<(out, v);
  return out;
}

#endif //__cplusplus
#endif // INC_KFD_OSTREAM_OPS_H_
 
