BEGIN {
     f = ARGV[1]
     i = 0
     while(getline <f)
	  a[i++] = $1
     n = i
     for (i=n-1; i>=1; i--)
     {
	  j = int((i+1) * rand())
	  t = a[j]
	  a[j] = a[i]
	  a[i] = t
     }
     for (i=0; i<n; i++)
	  print a[i]
}